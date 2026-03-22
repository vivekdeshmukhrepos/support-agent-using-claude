/**
 * Main JavaScript for Email Support Agent UI
 */

// Helper functions
function showAlert(message, type = 'success') {
    const alert = document.getElementById(`alert`);
    if (alert) {
        alert.textContent = message;
        alert.className = `alert show alert-${type}`;
        setTimeout(() => {
            alert.classList.remove('show');
        }, 5000);
    }
}

function showLoading(show = true) {
    const loading = document.getElementById('loading');
    if (loading) {
        loading.classList.toggle('show', show);
    }
}

function showResults(show = true) {
    const results = document.getElementById('result-container');
    if (results) {
        results.classList.toggle('show', show);
    }
}

// Test page functionality
async function submitEmail(event) {
    event.preventDefault();

    const sender = document.getElementById('sender')?.value;
    const recipient = document.getElementById('recipient')?.value;
    const subject = document.getElementById('subject')?.value;
    const body = document.getElementById('body')?.value;

    if (!sender || !recipient || !subject || !body) {
        showAlert('Please fill in all fields', 'error');
        return;
    }

    showLoading(true);
    showResults(false);

    try {
        const response = await fetch('/api/emails', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                sender,
                recipient,
                subject,
                body,
            }),
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || 'Failed to submit email');
        }

        // Display results
        displayEmailResults(data.email_id);
        document.getElementById('email-form')?.reset();
        showAlert('Email processed successfully!', 'success');

    } catch (error) {
        showAlert(error.message, 'error');
        console.error('Error:', error);
    } finally {
        showLoading(false);
    }
}

async function displayEmailResults(emailId) {
    try {
        const response = await fetch(`/api/emails/${emailId}`);
        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || 'Failed to fetch results');
        }

        // Update classification section
        const intentEl = document.getElementById('result-intent');
        const urgencyEl = document.getElementById('result-urgency');
        const categoryEl = document.getElementById('result-category');
        const confidenceEl = document.getElementById('result-confidence');

        if (intentEl) intentEl.textContent = data.intent || 'N/A';
        if (urgencyEl) urgencyEl.innerHTML = `<span class="badge badge-${getUrgencyClass(data.urgency)}">${data.urgency || 'N/A'}</span>`;
        if (categoryEl) categoryEl.textContent = data.category || 'N/A';
        if (confidenceEl) {
            const percentage = (data.confidence * 100).toFixed(1);
            confidenceEl.innerHTML = `
                <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                    <span>${percentage}%</span>
                </div>
                <div class="confidence-bar">
                    <div class="confidence-fill" style="width: ${percentage}%"></div>
                </div>
            `;
        }

        // Update status section
        const statusEl = document.getElementById('result-status');
        const escalatedEl = document.getElementById('result-escalated');
        const ticketEl = document.getElementById('result-ticket');

        if (statusEl) statusEl.innerHTML = `<span class="badge badge-${getStatusClass(data.final_status)}">${data.final_status || 'N/A'}</span>`;
        if (escalatedEl) escalatedEl.textContent = data.escalated ? 'Yes' : 'No';
        if (ticketEl) ticketEl.textContent = data.escalation_ticket_id || 'N/A';

        // Update response section
        const responseEl = document.getElementById('result-response');
        if (responseEl) {
            responseEl.textContent = data.draft_response || 'No response generated';
        }

        showResults(true);

    } catch (error) {
        showAlert('Failed to fetch email results: ' + error.message, 'error');
        console.error('Error:', error);
    }
}

// Dashboard page functionality
async function loadEmails() {
    try {
        const response = await fetch('/api/emails-list');
        const data = await response.json();

        displayEmailsTable(data.emails);
        updateDashboardStats(data);

    } catch (error) {
        showAlert('Failed to load emails: ' + error.message, 'error');
        console.error('Error:', error);
    }
}

function displayEmailsTable(emails) {
    const tbody = document.getElementById('emails-tbody');
    if (!tbody) return;

    if (!emails || emails.length === 0) {
        tbody.innerHTML = '<tr><td colspan="6" class="no-emails">No emails processed yet</td></tr>';
        return;
    }

    tbody.innerHTML = emails.map(email => `
        <tr>
            <td>
                <strong>${email.sender.substring(0, 20)}</strong><br>
                <span style="color: var(--secondary); font-size: 0.85rem;">${email.subject.substring(0, 30)}...</span>
            </td>
            <td>
                <span class="badge badge-${getStatusClass(email.state?.final_status || 'processing')}">
                    ${email.state?.final_status || 'processing'}
                </span>
            </td>
            <td>${email.state?.intent || 'N/A'}</td>
            <td>
                <span class="badge badge-${getUrgencyClass(email.state?.urgency || 'low')}">
                    ${email.state?.urgency || 'N/A'}
                </span>
            </td>
            <td>${email.state?.category || 'N/A'}</td>
            <td>
                <button class="btn btn-primary btn-small" onclick="viewEmailDetails('${email.email_id}')">
                    View Details
                </button>
            </td>
        </tr>
    `).join('');
}

function updateDashboardStats(data) {
    const totalEl = document.getElementById('stat-total');
    const sentEl = document.getElementById('stat-sent');
    const escalatedEl = document.getElementById('stat-escalated');
    const avgConfidenceEl = document.getElementById('stat-confidence');

    if (totalEl) totalEl.textContent = data.stats?.total || 0;
    if (sentEl) sentEl.textContent = data.stats?.sent || 0;
    if (escalatedEl) escalatedEl.textContent = data.stats?.escalated || 0;
    if (avgConfidenceEl) avgConfidenceEl.textContent = data.stats?.avg_confidence?.toFixed(2) || '0.00';
}

async function viewEmailDetails(emailId) {
    try {
        const response = await fetch(`/api/emails/${emailId}`);
        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || 'Failed to fetch email details');
        }

        displayEmailModal(data);

    } catch (error) {
        showAlert('Failed to load email details: ' + error.message, 'error');
        console.error('Error:', error);
    }
}

function displayEmailModal(emailData) {
    const modal = document.getElementById('email-detail-modal');
    const content = document.getElementById('modal-body');

    if (!content) return;

    const confidencePercentage = (emailData.confidence * 100).toFixed(1);

    content.innerHTML = `
        <div class="detail-row">
            <div>
                <div class="detail-label">From</div>
                <div class="detail-value">${emailData.email_id}</div>
            </div>
            <div>
                <div class="detail-label">Status</div>
                <div class="detail-value">
                    <span class="badge badge-${getStatusClass(emailData.final_status)}">
                        ${emailData.final_status}
                    </span>
                </div>
            </div>
        </div>

        <hr style="margin: 1.5rem 0; border: none; border-top: 1px solid var(--border);">

        <div>
            <h3 style="margin-bottom: 1rem; color: var(--dark);">Classification</h3>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
                <div>
                    <div class="detail-label">Intent</div>
                    <div class="detail-value">${emailData.intent}</div>
                </div>
                <div>
                    <div class="detail-label">Category</div>
                    <div class="detail-value">${emailData.category}</div>
                </div>
                <div>
                    <div class="detail-label">Urgency</div>
                    <div class="detail-value">
                        <span class="badge badge-${getUrgencyClass(emailData.urgency)}">
                            ${emailData.urgency}
                        </span>
                    </div>
                </div>
                <div>
                    <div class="detail-label">Confidence</div>
                    <div class="detail-value">
                        ${confidencePercentage}%
                        <div class="confidence-bar">
                            <div class="confidence-fill" style="width: ${confidencePercentage}%"></div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <hr style="margin: 1.5rem 0; border: none; border-top: 1px solid var(--border);">

        ${emailData.draft_response ? `
            <div>
                <h3 style="margin-bottom: 1rem; color: var(--dark);">Generated Response</h3>
                <div class="detail-value" style="background: var(--light); padding: 1rem; border-radius: 4px; line-height: 1.8;">
                    ${emailData.draft_response}
                </div>
            </div>
        ` : ''}

        ${emailData.escalation_ticket_id ? `
            <hr style="margin: 1.5rem 0; border: none; border-top: 1px solid var(--border);">
            <div>
                <h3 style="margin-bottom: 1rem; color: var(--dark);">Escalation Details</h3>
                <div>
                    <div class="detail-label">Ticket ID</div>
                    <div class="detail-value">${emailData.escalation_ticket_id}</div>
                </div>
            </div>
        ` : ''}
    `;

    if (modal) {
        modal.classList.add('show');
    }
}

function closeModal() {
    const modal = document.getElementById('email-detail-modal');
    if (modal) {
        modal.classList.remove('show');
    }
}

function getStatusClass(status) {
    switch (status) {
        case 'sent':
            return 'success';
        case 'escalated':
            return 'warning';
        case 'failed':
            return 'danger';
        case 'processing':
        default:
            return 'info';
    }
}

function getUrgencyClass(urgency) {
    switch (urgency) {
        case 'critical':
        case 'high':
            return 'danger';
        case 'medium':
            return 'warning';
        case 'low':
        default:
            return 'success';
    }
}

function setExampleEmail(example) {
    const examples = {
        'password': {
            sender: 'user@example.com',
            recipient: 'support@company.com',
            subject: 'Unable to reset my password',
            body: 'I tried to reset my password but did not receive the reset email. Can you help me regain access to my account?'
        },
        'billing': {
            sender: 'business@client.com',
            recipient: 'support@company.com',
            subject: 'Question about Pro plan pricing',
            body: 'Hi, I am interested in upgrading to the Pro plan. What are the exact features and can I upgrade mid-month?'
        },
        'critical': {
            sender: 'admin@company.com',
            recipient: 'support@company.com',
            subject: 'URGENT: Application is crashing',
            body: 'The application crashes immediately after login on all browsers. This is blocking our entire team. Please help ASAP!'
        }
    };

    const data = examples[example];
    if (data) {
        document.getElementById('sender').value = data.sender;
        document.getElementById('recipient').value = data.recipient;
        document.getElementById('subject').value = data.subject;
        document.getElementById('body').value = data.body;
    }
}

// Modal close on background click
document.addEventListener('click', function(event) {
    const modal = document.getElementById('email-detail-modal');
    if (event.target === modal) {
        closeModal();
    }
});

// Load emails on dashboard page load
document.addEventListener('DOMContentLoaded', function() {
    if (document.getElementById('emails-tbody')) {
        loadEmails();
        // Refresh emails every 10 seconds
        setInterval(loadEmails, 10000);
    }
});
