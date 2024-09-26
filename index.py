import os
import tkinter as tk
from tkinter import messagebox
from barcode import Code128
from barcode.writer import ImageWriter
from fpdf import FPDF

# Function to generate barcode images
def generate_barcode(data, output_image):
    barcode = Code128(data, writer=ImageWriter())
    barcode.save(output_image)
    print(f"Generated barcode saved as {output_image}")

# Function to get a unique file name
def get_unique_filename(base_name, extension):
    counter = 1
    unique_name = f"{base_name}{extension}"
    while os.path.exists(unique_name):
        unique_name = f"{base_name}_{counter}{extension}"
        counter += 1
    return unique_name

# Function to handle the button click event
def on_generate():
    barcode_data = entry.get()
    if not barcode_data:
        messagebox.showerror("Input Error", "Please enter the barcode data.")
        return

    output_image = os.path.join(os.getcwd(), "barcode")
    generate_barcode(barcode_data, output_image)

    output_image_path = output_image + ".png"
    if not os.path.exists(output_image_path):
        messagebox.showerror("Error", f"The image file '{output_image_path}' was not created.")
        return

    # Create a unique PDF name
    pdf_base_name = os.path.join(os.getcwd(), "barcode_output")
    pdf_output_path = get_unique_filename(pdf_base_name, ".pdf")

    # Create a PDF and add the barcode images
    pdf = FPDF()
    pdf.add_page()

    # Set the dimensions of the barcode in inches
    barcode_width = 1 * 25.4  # 1 inch in mm
    barcode_height = 1.5 * 25.4  # 1.5 inches in mm
    spacing = 5  # Spacing in mm between barcodes

    # Calculate how many barcodes fit on the page
    page_width = pdf.w - pdf.r_margin - pdf.l_margin
    page_height = pdf.h - pdf.b_margin - pdf.t_margin

    # Fill the page with barcodes with spacing
    for y in range(0, int(page_height // (barcode_height + spacing))):
        for x in range(0, int(page_width // (barcode_width + spacing))):
            pdf.image(output_image_path, 
                      x=x * (barcode_width + spacing) + pdf.l_margin, 
                      y=y * (barcode_height + spacing) + pdf.t_margin,
                      w=barcode_width, h=barcode_height)

    # Output the PDF file
    pdf.output(pdf_output_path)
    messagebox.showinfo("Success", f"PDF generated successfully: {pdf_output_path}")

# Create the main window
root = tk.Tk()
root.title("Barcode Generator")

# Create and place UI elements
tk.Label(root, text="Enter Barcode Data:").pack(pady=10)
entry = tk.Entry(root, width=30)
entry.pack(pady=10)
button = tk.Button(root, text="Generate Barcode and PDF", command=on_generate)
button.pack(pady=20)

# Start the GUI event loop
root.mainloop()
