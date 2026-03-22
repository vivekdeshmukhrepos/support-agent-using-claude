# UI Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Step 1: Load the Knowledge Base (Once)
```bash
python load_knowledge_base.py
```

Expected output:
```
Loading knowledge base from ./data_or_knowledge_graph/knowledge_base
Found 4 document files
Loaded 4 documents total
Split into 47 chunks
FAISS index saved to ./data_or_knowledge_graph/faiss_index
✅ Knowledge base loaded successfully!
```

### Step 2: Start the Application
```bash
python main.py
```

Expected output:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

### Step 3: Open Your Browser
Click one of these links (or copy to your browser):
- **Test Email Page**: http://localhost:8000/
- **Dashboard**: http://localhost:8000/dashboard

### Step 4: Test the System

#### Option A: Use Quick Examples
1. Go to http://localhost:8000/
2. Click one of the quick example buttons:
   - 📝 **Password Reset** - Account issue
   - 📝 **Billing Question** - Payment question
   - 📝 **Urgent Issue** - Critical problem
3. Click **Submit Email**
4. Watch the results load!

#### Option B: Submit Custom Email
1. Fill in the email form:
   - **From**: your@email.com
   - **To**: support@company.com (default)
   - **Subject**: Your question
   - **Body**: Detailed description
2. Click **Submit Email**
3. See results instantly

### Step 5: View Dashboard
1. Click **Dashboard** in the top menu
2. See statistics:
   - Total emails processed
   - Auto-replied count
   - Escalated count
   - Average confidence score
3. Browse all processed emails
4. Click **View Details** on any email

## 📋 What You'll See

### Test Page Results

```
📊 CLASSIFICATION RESULTS
├─ Intent: question
├─ Category: account
├─ Urgency: high
└─ Confidence: 92%

✅ PROCESSING STATUS
├─ Final Status: sent ✓
└─ Escalated to Human?: No

💬 GENERATED RESPONSE
"Dear Customer, I understand you're having trouble with your password.
Here's how to reset it: 1. Click 'Forgot Password' on the login page..."
```

### Dashboard View

```
📊 STATISTICS
┌─────────────┬──────────┬────────────┬──────────────┐
│ Total: 5    │ Sent: 3  │ Escalated: │ Confidence:  │
│ Emails      │ Auto     │ 2          │ 0.87         │
└─────────────┴──────────┴────────────┴──────────────┘

📧 EMAIL TABLE
┌─────────────┬──────────┬──────────┬─────────┬────────────┐
│ From/Subject│ Status   │ Intent   │ Urgency │ Category   │
├─────────────┼──────────┼──────────┼─────────┼────────────┤
│ john@ex...  │ ✓ sent   │ question │ high    │ account    │
│ jane@bu...  │ ✓ sent   │ request  │ low     │ billing    │
│ admin@c...  │ ⚠ urgent │ issue    │ critical│ technical  │
└─────────────┴──────────┴──────────┴─────────┴────────────┘

Click "View Details" on any email to see:
- Full classification results
- Retrieved documents from knowledge base
- Complete generated response
- Escalation ticket ID (if applicable)
```

## 🎯 Common Scenarios

### Scenario 1: Test Password Reset Email

```
1. Go to http://localhost:8000/
2. Click "Password Reset" button
3. Form auto-fills:
   From: user@example.com
   Subject: Unable to reset my password
   Body: I tried to reset my password but did not receive...

4. Click "Submit Email"

5. See results:
   Intent: question ✓
   Category: account ✓
   Urgency: high 🔴
   Confidence: 92% ████████████

6. View generated response from knowledge base
```

### Scenario 2: View Email History

```
1. Go to http://localhost:8000/dashboard
2. See statistics at top:
   - 5 Total Emails
   - 3 Auto-Replied
   - 2 Escalated
   - Avg Confidence: 0.87

3. Scroll through email table
4. Click "View Details" on any email
5. See full details in modal:
   - Classification scores
   - Retrieved documents
   - Generated response
   - Escalation info (if applicable)
```

### Scenario 3: Test Urgent/Escalation Email

```
1. Go to http://localhost:8000/
2. Click "Urgent Issue" button
3. Form auto-fills:
   Subject: URGENT: Application is crashing
   Body: The application crashes immediately after login...

4. Click "Submit Email"

5. See results:
   Intent: technical_issue
   Category: technical ✓
   Urgency: critical 🔴🔴
   Confidence: 94%

6. Notice:
   Escalation Status: ✓ Escalated to Human
   Ticket ID: email_xyz789

7. Go to dashboard to see it marked as "escalated"
```

## 🔧 Troubleshooting

### "Cannot GET /" - Page not found
```
❌ Problem: App isn't running
✅ Solution: Run: python main.py
```

### "Loading..." spinner never stops
```
❌ Problem: OPENAI_API_KEY not set
✅ Solution:
   1. Edit .env file
   2. Add: OPENAI_API_KEY=sk-your-actual-key-here
   3. Restart app
```

### Results show empty/missing fields
```
❌ Problem: Knowledge base not loaded
✅ Solution:
   1. Run: python load_knowledge_base.py
   2. Wait for "✅ Knowledge base loaded"
   3. Refresh page
```

### Styles look broken
```
❌ Problem: CSS file not loading
✅ Solution:
   1. Check console (F12 → Console)
   2. Ensure static/css/style.css exists
   3. Hard refresh page: Ctrl+Shift+R (or Cmd+Shift+R on Mac)
```

### Dashboard shows no emails
```
❌ Problem: First load, no emails processed
✅ Solution:
   1. Go to test page
   2. Submit at least one email
   3. Go back to dashboard
   4. Or wait for auto-refresh (10 seconds)
```

## 📱 Mobile Access

Want to test on your phone?

### Find Your Computer's IP
**Windows**:
```bash
ipconfig
# Look for "IPv4 Address" (usually 192.168.x.x)
```

**Mac/Linux**:
```bash
ifconfig
# Look for "inet" address (usually 192.168.x.x)
```

### Access from Phone
1. Make sure phone is on same WiFi
2. Open browser on phone
3. Go to: `http://192.168.x.x:8000`
4. Enjoy responsive design!

## ✅ Checklist

Before you start, make sure:

- [ ] Python 3.12+ is installed
- [ ] Virtual environment is activated
- [ ] Requirements installed: `pip install -r requirements.txt`
- [ ] .env file created with OPENAI_API_KEY
- [ ] Knowledge base loaded: `python load_knowledge_base.py`
- [ ] App started: `python main.py`
- [ ] Browser can access: http://localhost:8000

## 📞 Need Help?

See these guides for more info:
- **Full UI Guide**: [UI_GUIDE.md](UI_GUIDE.md)
- **FAISS Setup**: [FAISS_GUIDE.md](FAISS_GUIDE.md)
- **API Reference**: [README.md](README.md)

## 🎉 You're Ready!

The UI is now ready to test. Go to http://localhost:8000 and start testing emails!

---

**Pro Tips:**
- Use Dashboard to monitor all emails
- Try different urgency levels to see escalations
- View Details to understand classification reasoning
- Check knowledge base matches for accuracy
- Refresh dashboard or auto-refresh after submissions
