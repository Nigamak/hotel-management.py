import cv2
from pyzbar.pyzbar import decode
import numpy as np

def barcode_scanner():
    # Initialize the camera
    cap = cv2.VideoCapture(0)
    
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        
        # Convert frame to grayscale for better barcode detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Detect barcodes in the grayscale frame
        barcodes = decode(gray)
        
        # Loop over detected barcodes
        for barcode in barcodes:
            # Extract barcode data
            data = barcode.data.decode('utf-8')
            
            # Extract barcode bounding box coordinates
            (x, y, w, h) = barcode.rect
            
            # Draw bounding box around the barcode
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            
            # If the detected barcode matches the specified barcode
            if data == "suitesavvy-1-301":
                cv2.putText(frame, "Room Unlocked", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        # Display the frame
        cv2.imshow('Barcode Scanner', frame)
        
        # Quit if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # Release the camera and close all windows
    cap.release()
    cv2.destroyAllWindows()

# Call the barcode scanner function
barcode_scanner()