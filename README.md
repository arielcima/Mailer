# Mailer Tkinter Application

This is a Python GUI application built with `tkinter` that allows you to easily send bulk emails to a list of recipients. It supports rich text (HTML format), image embedding through Content-ID, clickable links, and multiple file attachments.

## Features
- **Graphical User Interface:** Simple Tkinter UI.
- **Rich Emails:** Embed a company logo or image and link it to a URL.
- **Bulk Deliveries:** Load a list of recipients from a plain text file (one address per line).
- **Asynchronous Sending:** Progress is shown via a progress bar running on a separate thread, keeping the app responsive.
- **Attachment Support:** Select local files and attach them to the outgoing emails.

## Prerequisites
- Python 3.x
- Access to an SMTP server

## Setup
1. Clone the repository.
   ```bash
   git clone https://github.com/yourusername/Mailer.git
   cd Mailer
   ```
2. Create and activate a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   # Depending on your OS:
   venv\Scripts\activate     # Windows
   # source venv/bin/activate # macOS/Linux
   ```
3. Copy the environment configuration template:
   ```bash
   copy .env.example .env    # Windows
   # cp .env.example .env    # macOS/Linux
   ```
4. Open the `.env` file and configure your SMTP variables:
   - `SMTP_SERVER`: The FQDN of your mail server (e.g., `smtp.gmail.com`)
   - `SMTP_PORT`: SMTP port (e.g. 25, 587)
   - `SENDER_EMAIL`: The originating email address.

## Usage
1. Run the application:
   ```bash
   python mailer.py
   ```
2. Enter your subject and body.
3. To embed an image, check **Agregar Imagen**, browse for an image file, and set a link.
4. Add file attachments by clicking **Adjuntar Archivos**.
5. When ready, click **Enviar Mails**. You will be prompted to select a `.txt` file containing the recipient email addresses.
6. A progress window will track the status of sending. You can cancel at any time.

## Testing Locally
If you want to test the application without sending actual emails, you can run the included `fake_smtp.py` script. It acts as a local dummy SMTP server that captures outgoing emails and prints them to the console instead of delivering them.

1. Open a new terminal and start the fake SMTP server:
   ```bash
   python fake_smtp.py
   ```
2. The server will listen on `127.0.0.1` port `25` (which are the default fallback values if no `.env` is configured).
3. Run the `mailer.py` application normally and send your emails.
4. You will see the incoming emails printed in the terminal where `fake_smtp.py` is running. Press `Ctrl+C` in that terminal to stop the server when you are done testing.
