import time

import cv2
import numpy as np
from pyzbar.pyzbar import decode
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import shutil

# Global variable for event_key
event_key = ""
file_name = ""
event_key_file = "event_key.txt"  # File to store the event_key

def load_event_key():
    """Load the event_key from a file if it exists."""
    global event_key
    if os.path.exists(event_key_file):
        with open(event_key_file, 'r') as file:
            event_key = file.read().strip()


def save_event_key():
    """Save the event_key to a file."""
    with open(event_key_file, 'w') as file:
        file.write(event_key)

def handle_qr_data(qr_data, isSpace):
    """Function to handle QR code data when Space key is pressed."""
    #Wrap everything in a try, so if we see random data we are okay.
    global hasQRCode, last_char_time
    #Check if the space is WITHIN the QR code. If so, don't try this!
    if (time.time() - last_char_time) > 0.1:
        if hasQRCode:
            #try:
            # Split the content by '%'
            sections = qr_data.split('%')

            # Extract the generic data section and split by '$'
            generic_data = sections[0].split('$')

            # Extract the matchId from the generic data
            match_id = _extract_numbers(next((element for element in generic_data if element.startswith('B')), ''))

            team_number = ''
            collection_mode = 'Subjective' if qr_data.startswith('*') else 'Objective'

            if collection_mode == 'Objective':
                # Extract the objective data section and split by '$'
                try:
                    print(sections)
                    objective_data = sections[1].split('$')

                    for element in objective_data:
                        if element.startswith('Z'):
                            team_number = _extract_numbers(element)
                except IndexError as e:
                    messagebox.showerror("Data has no team number!" + e)
            else:
                # Extract the team number based on the subjective collection mode
                team_number = 'Red' if generic_data[0].startswith('F') and generic_data[0].endswith('TRUE') else 'Blue'

            # Update fileName and fileContent
            global file_name
            #preface with timestamp
            timestamp = time.strftime("%Y%m%d%H%M%S")
            file_name = f'{timestamp}_{match_id}_{team_number}_{event_key}_{collection_mode}.txt'
            hasQRCode = True
            if isSpace:  # actually save
                save_qr_data(qr_data)
            #except Exception as e:
            #    messagebox.showerror("Error", e)
        else:
            messagebox.showerror("Error", "No QR code detected")


def _extract_numbers(string):
    return ''.join(filter(str.isdigit, string))


def save_qr_data(qr_data):
    """Save QR code data to the appropriate file based on drive availability."""
    global file_name, hasQRCode
    hasQRCode = False
    if event_key == "":
        messagebox.showerror("Error", f"FIRST SET EVENT KEY IN SETTINGS!")
        return
    usb_drive_path = f'E:/data/{file_name}'
    documents_path = f'QRCodeOutputs/{file_name}'
    override = False
    # Check if USB drive is available
    if os.path.exists('E:/'):
        file_path = usb_drive_path
    else:
        override = True
        file_path = documents_path
        os.makedirs(os.path.dirname(documents_path), exist_ok=True)  # Create directory if not exists

    with open(file_path, 'w') as file:
        file.write(f"{qr_data}\n")
    if not override:
        #save locally as well
        with open(f"QRCodeOutputs/{file_name}", 'w') as file:
            file.write(f"{qr_data}\n")
    messagebox.showinfo("Success", f"QR code data saved successfully to {file_path}")
    current_qr_data = None


def open_qrcode_folder():
    """Open the QRCodeOutputs folder in the file explorer."""
    documents_path = 'QRCodeOutputs'
    if os.name == 'nt':  # For Windows
        os.startfile(documents_path)


def open_usb_folder():
    usb_drive_path = 'E:/data'
    if not os.path.exists(usb_drive_path):
        messagebox.showerror("Error", "USB drive not found.")
        return
    if os.name == 'nt':  # For Windows
        os.startfile(usb_drive_path)


def move_local_data_to_usb():
    """Move files from the local data path to the USB drive, avoiding duplicates."""
    usb_drive_path = 'E:/data'
    local_data_path = 'QRCodeOutputs'

    if not os.path.exists(usb_drive_path):
        messagebox.showerror("Error", "USB drive not found.")
        return

    os.makedirs(usb_drive_path, exist_ok=True)

    usb_files = set(os.listdir(usb_drive_path))

    local_files = os.listdir(local_data_path)

    something_moved = False
    for file_name in local_files:
        local_file_path = os.path.join(local_data_path, file_name)
        usb_file_path = os.path.join(usb_drive_path, file_name)
        print(file_name)
        if file_name not in usb_files:
            shutil.copy(local_file_path, usb_file_path)
            something_moved = True
            print(f"Moved: {file_name}")
        else:
            print(f"Skipped (already exists on USB): {file_name}")
    if something_moved:
        messagebox.showinfo("Success", "New local data copied to USB drive.")

current_qr_data = ""
def update_frame():
    """Capture a frame from the webcam, process it, and update the tkinter canvas."""
    global current_qr_data, hasQRCode

    # Capture frame-by-frame
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        root.after(10, update_frame)
        return

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect QR codes
    decoded_objects = decode(gray)
    qr_type = None
    qr_data = None
    for obj in decoded_objects:
        # Draw a rectangle around the QR code
        points = obj.polygon
        if len(points) == 4:
            pts = np.array(points, dtype=np.int32)
            pts = pts.reshape((-1, 1, 2))
            cv2.polylines(frame, [pts], True, (0, 255, 0), 2)
        else:
            hull = cv2.convexHull(np.array(points, dtype=np.float32))
            cv2.polylines(frame, [np.int32(hull)], True, (0, 255, 0), 2)

        # Decode the QR code data
        qr_data = obj.data.decode('utf-8')
        qr_type = obj.type


        # Update the current QR code data
        current_qr_data = qr_data
        hasQRCode = True
        # Display QR code data
    text = ""
    if current_qr_data is not None and hasQRCode:
        handle_qr_data(current_qr_data, False)
        if qr_type is not None:
            text = f"{qr_type}: {file_name}"
        else:
            text = f"Scanner: {file_name}"
    cv2.putText(frame, text, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    pil_image = Image.fromarray(frame_rgb)
    tk_image = ImageTk.PhotoImage(image=pil_image)

    canvas.create_image(0, 0, anchor=tk.NW, image=tk_image)
    canvas.image = tk_image

    check_usb_drive()

    root.after(10, update_frame)


def check_usb_drive():
    """Check if USB drive is available and update the checkbox state."""
    if os.path.exists('E:/'):
        usb_drive_checkbox.config(text="USB Drive Available",bg='green')  # Green if USB drive is present
    else:
        usb_drive_checkbox.config(text="USB Drive Unavailable",bg='red')  # Red if USB drive is not present


def open_settings():
    """Function to open the settings window."""
    global event_key

    def save_settings():
        global event_key
        event_key = event_key_entry.get()
        save_event_key()
        settings_window.destroy()

    settings_window = tk.Toplevel()
    settings_window.title("Settings")

    # Create a label and text input for the event_key
    tk.Label(settings_window, text="Event Key:").pack(pady=10)
    event_key_entry = tk.Entry(settings_window)
    event_key_entry.insert(0, event_key)  # Set the initial value
    event_key_entry.pack(pady=5)

    # Create a save button
    tk.Button(settings_window, text="Save", command=save_settings).pack(pady=10)
def toggle_fullscreen(event=None):
    global fullscreen
    fullscreen = not fullscreen
    root.attributes('-fullscreen', fullscreen)
    root.bind('<Escape>', end_fullscreen)

def end_fullscreen(event=None):
    global fullscreen
    fullscreen = False
    root.attributes('-fullscreen', False)
    root.bind('<F11>', toggle_fullscreen)
fullscreen = False
QRtext = ""
last_char_time = time.time()
hasQRCode = False


# Function to process each keypress as part of QR code scan
def on_key_press(event):
    global QRtext, last_char_time, hasQRCode, current_qr_data

    now = time.time()
    char = event.char  # Get the character from the event

    # Check if the character is part of a continuous QR code scan (within 50 ms)
    if now - last_char_time < 0.1:
        QRtext += char  # Append to QR code text
    else:
        QRtext = char  # Reset QR code text if time exceeds threshold

    last_char_time = now

    # If Enter key is pressed, assume QR code is complete
    if event.keysym == 'Return':
        if len(QRtext) > 15:
            print("GOT QR CODE! " + QRtext)
            hasQRCode = True
            current_qr_data = QRtext  # Set current QR data to display
            QRtext = ""  # Reset QR text for next scan

def main():
    global cap, root, canvas, current_qr_data, usb_drive_checkbox
    load_event_key()
    # Open the webcam
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    current_qr_data = None

    # Create the main window
    root = tk.Tk()
    root.title("QR Code Reader")
    root.geometry("1280x720")
    canvas = tk.Canvas(root, width=1280, height=720)
    canvas.pack(fill=tk.BOTH, expand=True)
    # Initialize fullscreen mode
    fullscreen = True
    root.attributes('-fullscreen', fullscreen)
    root.bind('<F11>', toggle_fullscreen)
    root.bind('<Escape>', end_fullscreen)
    # Create a button to open settings
    settings_button = tk.Button(root, text="Settings", command=open_settings)
    settings_button.place(x=10, y=800, anchor='sw')

    # Create a checkbox to show USB drive status
    usb_drive_checkbox = tk.Label(root, text="USB Drive Unavailable", width=20, height=2, bg="red", fg='white')
    usb_drive_checkbox.place(x=10, y=760, anchor='sw')

    # Create a button to open the QRCodeOutputs folder
    open_folder_button = tk.Button(root, text="Open QR Code Outputs Folder", command=open_qrcode_folder)
    open_folder_button.place(x=10, y=720, anchor='sw')
    open_usb_button = tk.Button(root, text="Open USB Drive", command=open_usb_folder)
    open_usb_button.place(x=10, y=680, anchor='sw')
    # Create a button to move local data to USB
    move_data_button = tk.Button(root, text="Move Local Data To USB", command=move_local_data_to_usb)
    move_data_button.place(x=10, y=640, anchor='sw')


    root.bind('<space>', lambda event: handle_qr_data(current_qr_data, True) if current_qr_data else None)
    #read all input for QRCode
    root.bind('<Key>', on_key_press)
    update_frame()

    root.mainloop()


if __name__ == "__main__":
    main()
