# Web UI Guide - Email Support Agent

## Overview

A modern, responsive web interface for testing and managing the email support agent. Built with vanilla JavaScript, HTML, and CSS (no external frameworks).

## Features

### 🧪 Test Page (`/`)
- **Submit Mock Emails**: Test the system with custom emails
- **Quick Examples**: Pre-filled templates for common scenarios
- **Live Results**: See classification, retrieved documents, and generated responses
- **Real-time Processing**: Watch emails process through the pipeline

### 📊 Dashboard (`/dashboard`)
- **Email History**: View all processed emails
- **Statistics**: Total emails, auto-replied, escalated, average confidence
- **Detailed View**: Click to see complete email details and agent output
- **Auto-refresh**: Updates every 10 seconds

## Architecture

```
Frontend (HTML/CSS/JavaScript)
    ↓
FastAPI Routes (ui.py)
    ↓
Email Service / Graph
    ↓
Results
```

### File Structure
```
static/
├── css/
│   └── style.css          # All styling (responsive, modern design)
└── js/
    └── main.js            # All JavaScript (form handling, API calls, modals)

templates/
├── base.html              # Base layout with navbar
├── test.html              # Test email page
└── dashboard.html         # Email history dashboard

src/api/routes/
└── ui.py                  # FastAPI routes for UI pages and API
```

## Pages

### 1. Test Email Page (`GET /`)

**Purpose**: Submit and test emails with immediate feedback

**Components**:
- Email form with fields: Sender, Recipient, Subject, Body
- Quick example buttons (Password Reset, Billing Question, Urgent Issue)
- Live classification results with visual indicators
- Retrieved documents section
- Generated response preview
- Escalation status

**Flow**:
```
User fills form
    ↓
Click "Submit Email"
    ↓
API: POST /api/emails
    ↓
Graph processes email
    ↓
API: GET /api/emails/{email_id}
    ↓
Display results in real-time
```

**Example**:
```
Input:
  From: customer@example.com
  Subject: Unable to reset my password
  Body: I tried to reset but didn't receive the email

Output:
  Intent: question ✓
  Urgency: high 🔴
  Category: account ✓
  Confidence: 92% ████████████

  Retrieved Documents:
  - Password reset instructions
  - Account verification info

  Generated Response:
  "Hello! I understand you're having trouble resetting your password..."
```

### 2. Dashboard Page (`GET /dashboard`)

**Purpose**: Monitor all processed emails and view statistics

**Components**:
- Statistics cards (Total, Auto-Replied, Escalated, Avg Confidence)
- Responsive email table with columns:
  - From/Subject
  - Status (badge)
  - Intent
  - Urgency (badge)
  - Category
  - Actions (View Details button)
- Detail modal for full email information
- Auto-refresh (every 10 seconds)

**Email Table Columns**:
| Column | Type | Shows |
|--------|------|-------|
| From/Subject | Text | Sender email and subject preview |
| Status | Badge | sent, escalated, processing, failed |
| Intent | Text | question, complaint, request, etc. |
| Urgency | Badge | Color-coded: low, medium, high, critical |
| Category | Text | billing, technical, account, etc. |
| Actions | Button | Click to view full details |

**Detail Modal**:
- Complete email metadata
- Classification details with confidence bar
- Generated response text
- Escalation ticket ID (if applicable)
- Close button or click outside to close

## API Endpoints

### POST /api/emails
Submit an email for processing

**Request**:
```json
{
  "sender": "customer@example.com",
  "recipient": "support@company.com",
  "subject": "Email subject",
  "body": "Email message body"
}
```

**Response**:
```json
{
  "email_id": "email_abc123",
  "status": "sent",
  "message": "Email processed successfully. Status: sent"
}
```

### GET /api/emails/{email_id}
Get detailed status of a specific email

**Response**:
```json
{
  "email_id": "email_abc123",
  "status": "sent",
  "intent": "question",
  "urgency": "high",
  "category": "account",
  "confidence": 0.92,
  "final_status": "sent",
  "escalated": false,
  "escalation_ticket_id": null,
  "draft_response": "Generated response text..."
}
```

### GET /api/emails-list
Get all emails with statistics (for dashboard)

**Response**:
```json
{
  "emails": [
    {
      "email_id": "email_abc123",
      "sender": "customer@example.com",
      "recipient": "support@company.com",
      "subject": "Email subject",
      "state": {
        "intent": "question",
        "urgency": "high",
        "category": "account",
        "confidence": 0.92,
        "final_status": "sent",
        "draft_response": "..."
      }
    }
  ],
  "stats": {
    "total": 5,
    "sent": 3,
    "escalated": 2,
    "avg_confidence": 0.87
  }
}
```

## Quick Start

### 1. Load Knowledge Base
```bash
python load_knowledge_base.py
```

### 2. Start the Application
```bash
python main.py
```

Output:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

### 3. Open in Browser
- **Test Page**: http://localhost:8000/
- **Dashboard**: http://localhost:8000/dashboard

## Usage Examples

### Example 1: Test Password Reset Email

1. Go to http://localhost:8000/
2. Click "Password Reset" quick example
3. Click "Submit Email"
4. View results:
   - Classification: intent=question, category=account, urgency=high
   - Retrieved docs from knowledge base
   - Generated response based on FAQ

### Example 2: View Email History

1. Go to http://localhost:8000/dashboard
2. See statistics at the top
3. Browse emails in the table
4. Click "View Details" to see full email information
5. Dashboard auto-refreshes every 10 seconds

### Example 3: Test Custom Email

1. Go to http://localhost:8000/
2. Fill in custom email details:
   - Sender: your@email.com
   - Recipient: support@company.com
   - Subject: Your question
   - Body: Detailed description
3. Click "Submit Email"
4. See real-time processing and results

## Design Features

### Responsive Design
- Works on desktop, tablet, and mobile
- Adapts layout for smaller screens
- Touch-friendly buttons and forms

### Color Coding
- **Green**: Success, low urgency, good confidence
- **Blue**: Info, processing status
- **Orange/Yellow**: Medium urgency, warnings
- **Red**: Danger, high/critical urgency, errors

### Visual Feedback
- Loading spinner during processing
- Toast notifications for success/error
- Confidence bars with visual representation
- Status badges with appropriate colors
- Smooth animations and transitions

### Accessibility
- Semantic HTML
- Good contrast ratios
- Clear labels for form fields
- Keyboard navigation support

## Customization

### Change Colors
Edit `static/css/style.css` at the top:
```css
:root {
    --primary: #2563eb;      /* Main button color */
    --success: #16a34a;      /* Success/green */
    --warning: #ea580c;      /* Warning/orange */
    --danger: #dc2626;       /* Danger/red */
    /* ... more colors ... */
}
```

### Adjust Refresh Rate
Edit `static/js/main.js`:
```javascript
// Change 10000 (10 seconds) to your preferred interval
setInterval(loadEmails, 10000);
```

### Customize Quick Examples
Edit `static/js/main.js` in the `setExampleEmail()` function:
```javascript
const examples = {
    'password': { /* ... */ },
    'billing': { /* ... */ },
    'critical': { /* ... */ },
    'custom': { /* Add your own */ }
};
```

## Troubleshooting

### Issue: Page shows "Templates directory not found"
**Solution**: Ensure `templates/` directory exists in the project root
```bash
mkdir -p templates
```

### Issue: Styles not loading
**Solution**: Ensure `static/` directory exists with `css/` and `js/` subdirectories
```bash
mkdir -p static/css static/js
```

### Issue: API calls failing (404)
**Solution**:
- Ensure the app is running: `python main.py`
- Check that OPENAI_API_KEY is set in `.env`
- Check browser console for specific error

### Issue: Dashboard shows "No emails processed yet"
**Solution**:
- Go to test page and submit an email first
- Dashboard auto-refreshes every 10 seconds
- Or refresh manually with F5

### Issue: Modal not closing
**Solution**:
- Click the × button in top-right corner
- Click outside the modal (on dark background)
- Check browser console for errors

## Performance Notes

- **Test Page**: <100ms to display results (after LLM processing)
- **Dashboard Load**: <200ms to fetch all emails
- **Auto-refresh**: Every 10 seconds (adjustable)
- **Modal Open/Close**: Instant
- **In-memory Storage**: No database calls (uses Python dict)

## Browser Support

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+
- Mobile browsers (iOS Safari 14+, Chrome Mobile)

## Security Notes

- No authentication/authorization (local testing only)
- Email data stored in-memory (lost on server restart)
- No HTTPS (use on trusted networks only)
- For production: Add auth, use database, implement HTTPS

## Future Enhancements

1. **Authentication**: Add user login/roles
2. **Database**: Replace in-memory storage with PostgreSQL
3. **Export**: Export email data as CSV/PDF
4. **Filters**: Filter emails by status, urgency, date range
5. **Search**: Search emails by sender, subject, content
6. **Charts**: Visual graphs for statistics
7. **Email Integration**: Real IMAP/SMTP integration
8. **Webhooks**: External system notifications
9. **API Keys**: Create API keys for external integrations
10. **Rate Limiting**: Add request rate limiting

## Testing

### Manual Testing Checklist

- [ ] Test page loads without errors
- [ ] Submit form with valid data
- [ ] See loading spinner during processing
- [ ] Results display correctly
- [ ] Quick example buttons work
- [ ] Escalation shows for urgent emails
- [ ] Dashboard loads and shows statistics
- [ ] View details modal opens/closes
- [ ] Email table displays all processed emails
- [ ] Auto-refresh works (check 10 seconds after submission)
- [ ] Mobile view is responsive
- [ ] All buttons are clickable

### Browser Developer Tools

1. Open DevTools (F12)
2. Check Console tab for errors
3. Check Network tab for API calls
4. Monitor performance and load times
5. Test responsive design (Ctrl+Shift+M)

## References

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Jinja2 Templates](https://jinja.palletsprojects.com/)
- [MDN Web Docs](https://developer.mozilla.org/en-US/)
- [CSS Basics](https://developer.mozilla.org/en-US/docs/Web/CSS)
- [JavaScript Fetch API](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API)
