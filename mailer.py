import os
import smtplib
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
from email import encoders
from threading import Thread

# Default SMTP configuration with environment variable overrides
SMTP_SERVER = os.environ.get("SMTP_SERVER", "FQDN of mail server")
SMTP_PORT = int(os.environ.get("SMTP_PORT", 25))
SENDER_EMAIL = os.environ.get("SENDER_EMAIL", "[EMAIL_ADDRESS]")

class EmailSenderApp:
    """
    Main Tkinter application for sending bulk emails.
    """
    def __init__(self, root):
        self.root = root
        self.root.title("Email Sender")
        self.root.geometry("400x450")

        # Variables
        self.add_image = tk.BooleanVar()
        self.add_image_link_var = tk.BooleanVar()
        self.sending_cancelled = False

        # Pre-declare widget attributes to resolve linter warnings
        self.subject_entry: tk.Entry
        self.body_entry: tk.Text
        self.browse_button: tk.Button
        self.image_path_label: tk.Label
        self.image_path_entry: tk.Entry
        self.image_link_entry: tk.Entry
        self.attached_files_text: tk.Text
        self.progress_window: tk.Toplevel
        self.progress_label: tk.Label
        self.progress_bar: ttk.Progressbar
        self.ok_button: tk.Button
        self.cancel_button: tk.Button

        self._create_widgets()

    def _create_widgets(self):
        # Subject
        tk.Label(self.root, text="Asunto:").place(x=4, y=0)
        self.subject_entry = tk.Entry(self.root)
        self.subject_entry.place(x=4, y=20)

        # Body
        tk.Label(self.root, text="Cuerpo:").place(x=4, y=40)
        self.body_entry = tk.Text(self.root, height=5)
        self.body_entry.place(x=4, y=60)

        # Add Image Checkbox
        tk.Checkbutton(self.root, text="Agregar Imagen", variable=self.add_image, 
                       command=self.toggle_image_widgets).place(x=4, y=150)

        # Browse Image Button
        self.browse_button = tk.Button(self.root, text="Buscar", command=self.browse_image, state=tk.DISABLED)
        self.browse_button.place(x=215, y=175)

        # Image Path
        self.image_path_label = tk.Label(self.root, text="Ruta Imagen:", state=tk.DISABLED)
        self.image_path_label.place(x=4, y=178)
        self.image_path_entry = tk.Entry(self.root, state=tk.DISABLED)
        self.image_path_entry.place(x=80, y=178)

        # Add Image Link Checkbox
        tk.Checkbutton(self.root, text="Agregar Enlace", variable=self.add_image_link_var, 
                       command=self.toggle_image_link_field).place(x=4, y=200)

        # Image Link
        self.image_link_entry = tk.Entry(self.root, state=tk.DISABLED)
        self.image_link_entry.place(x=80, y=228)
        tk.Label(self.root, text="Enlace:").place(x=4, y=225)

        # Attached Files
        tk.Label(self.root, text="Archivos Adjuntos:").place(x=4, y=255)
        self.attached_files_text = tk.Text(self.root, height=5)
        self.attached_files_text.place(x=4, y=275)

        # Action Buttons
        tk.Button(self.root, text="Adjuntar Archivos", command=self.attach_files).place(x=4, y=370)
        tk.Button(self.root, text="Enviar Mails", command=self.send_email).place(x=290, y=370)

        self.toggle_image_widgets()
        self.toggle_image_link_field()

    def toggle_image_widgets(self):
        state = tk.NORMAL if self.add_image.get() else tk.DISABLED
        self.image_path_label.config(state=state)
        self.image_path_entry.config(state=state)
        self.browse_button.config(state=state)

    def toggle_image_link_field(self):
        state = tk.NORMAL if self.add_image_link_var.get() else tk.DISABLED
        self.image_link_entry.config(state=state)

    def browse_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        if file_path:
            self.image_path_entry.delete(0, tk.END)
            self.image_path_entry.insert(tk.END, file_path)

    def attach_files(self):
        file_paths = filedialog.askopenfilenames()
        for file_path in file_paths:
            self.attached_files_text.insert(tk.END, file_path + "\n")

    def _create_email_message(self, subject, body, image_path, image_link, attached_files):
        """Constructs and returns the MIMEMultipart email object."""
        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = SENDER_EMAIL

        if self.add_image.get() and os.path.exists(image_path):
            html = f"""\
            <html>
              <body>
                <p>{body}</p>
                <a href="{image_link}"><img src="cid:image1"></a>
              </body>
            </html>
            """
            msg.attach(MIMEText(html, 'html'))

            with open(image_path, 'rb') as file:
                img_data = file.read()
            image = MIMEImage(img_data, name=os.path.basename(image_path))
            image.add_header('Content-ID', '<image1>')
            msg.attach(image)
        else:
            html = f"""\
            <html>
              <body>
                <p>{body}</p>
              </body>
            </html>
            """
            msg.attach(MIMEText(html, 'html'))

        for file_path in attached_files:
            if not os.path.exists(file_path):
                continue
            part = MIMEBase('application', 'octet-stream')
            with open(file_path, 'rb') as file:
                part.set_payload(file.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment', filename=str(os.path.basename(file_path)))
            msg.attach(part)

        return msg

    def send_email(self):
        subject = self.subject_entry.get()
        body = self.body_entry.get("1.0", "end-1c")
        image_path = self.image_path_entry.get()
        image_link = self.image_link_entry.get()
        attached_files = self.attached_files_text.get("1.0", "end-1c").splitlines()

        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if not file_path:
            return

        with open(file_path, "r") as file:
            addresses = file.read().splitlines()

        if not addresses:
            messagebox.showwarning("Warning", "The selected file is empty or invalid.")
            return

        msg = self._create_email_message(subject, body, image_path, image_link, attached_files)

        # Progress window setup
        self.progress_window = tk.Toplevel(self.root)
        self.progress_window.title("Sending Email Progress")
        self.progress_window.geometry("300x100")

        self.progress_label = tk.Label(self.progress_window, text="Sending emails...")
        self.progress_label.pack()

        self.progress_bar = ttk.Progressbar(self.progress_window, length=200, mode="determinate")
        self.progress_bar.pack()

        self.ok_button = tk.Button(self.progress_window, text="Ok", state=tk.DISABLED, command=self.progress_window.destroy)
        self.ok_button.pack(side=tk.LEFT)
        
        self.cancel_button = tk.Button(self.progress_window, text="Cancel", state=tk.NORMAL, command=self._cancel_sending)
        self.cancel_button.pack(side=tk.RIGHT)

        self.sending_cancelled = False

        # Launch thread to prevent blocking the GUI loop
        Thread(target=self._send_emails_thread, args=(addresses, msg)).start()

    def _cancel_sending(self):
        self.sending_cancelled = True

    def _send_emails_thread(self, addresses, msg):
        total_addresses = len(addresses)
        self.progress_bar["maximum"] = total_addresses

        for i, address in enumerate(addresses, start=1):
            if self.sending_cancelled:
                break

            try:
                with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as smtp:
                    smtp.sendmail(SENDER_EMAIL, address, msg.as_string())
                print(f"Email sent to: {address}")
            except smtplib.SMTPException as e:
                print(f"Failed to send email to: {address}")
                print(str(e))
            except Exception as e:
                print(f"Unexpected error: {str(e)}")

            self.progress_bar["value"] = i
            # Force GUI updates to render progress correctly
            self.progress_window.update()

        if self.sending_cancelled:
            self.progress_label.config(text="Email sending cancelled!")
        else:
            self.progress_label.config(text="Emails sent successfully!")
            self.ok_button.config(state=tk.NORMAL)
            self.cancel_button.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = EmailSenderApp(root)
    root.mainloop()