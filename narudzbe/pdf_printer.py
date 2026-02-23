#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PDF Printer for Appointment System
Generates and prints appointment PDFs using ReportLab
"""

import os
import sys
import platform
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

class AppointmentPrinter:
    """PDF printer for appointments with automatic print support"""
    
    def __init__(self, output_dir="output"):
        self.output_dir = output_dir
        self.page_width, self.page_height = A4
        
        # Create output directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
    
    def generate_appointment_pdf(self, appointment_data, filename=None):
        """
        Generate PDF for a single appointment
        
        Args:
            appointment_data (dict): Dictionary containing appointment information
            filename (str): Optional filename, auto-generated if not provided
            
        Returns:
            str: Path to generated PDF file
        """
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            customer_name = appointment_data.get('customer_name', 'Unknown').replace(' ', '_')
            filename = f"appointment_{customer_name}_{timestamp}.pdf"
        
        filepath = os.path.join(self.output_dir, filename)
        
        # Create PDF canvas
        c = canvas.Canvas(filepath, pagesize=A4)
        
        # Set title
        c.setTitle(f"Appointment - {appointment_data.get('customer_name', 'N/A')}")
        
        # Draw header
        self._draw_header(c)
        
        # Draw appointment details
        y_position = self.page_height - 5*cm
        y_position = self._draw_appointment_details(c, appointment_data, y_position)
        
        # Draw footer
        self._draw_footer(c)
        
        # Save PDF
        c.save()
        
        return filepath
    
    def _draw_header(self, c):
        """Draw PDF header"""
        c.setFont("Helvetica-Bold", 20)
        c.drawString(2*cm, self.page_height - 3*cm, "AUTO SERVIS - NARUDZBA")
        
        c.setFont("Helvetica", 10)
        c.drawString(2*cm, self.page_height - 3.5*cm, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Draw horizontal line
        c.setStrokeColor(colors.black)
        c.setLineWidth(2)
        c.line(2*cm, self.page_height - 4*cm, self.page_width - 2*cm, self.page_height - 4*cm)
    
    def _draw_appointment_details(self, c, data, start_y):
        """Draw appointment details on PDF"""
        c.setFont("Helvetica-Bold", 12)
        y = start_y
        
        # Customer Information
        c.drawString(2*cm, y, "CUSTOMER INFORMATION")
        y -= 0.7*cm
        
        c.setFont("Helvetica", 10)
        fields = [
            ("Customer Name:", data.get('customer_name', 'N/A')),
            ("Phone:", data.get('phone', 'N/A')),
            ("Email:", data.get('email', 'N/A')),
            ("Vehicle:", data.get('vehicle', 'N/A')),
            ("License Plate:", data.get('license_plate', 'N/A')),
        ]
        
        for label, value in fields:
            c.drawString(2.5*cm, y, label)
            c.drawString(6*cm, y, str(value))
            y -= 0.6*cm
        
        y -= 0.5*cm
        
        # Appointment Details
        c.setFont("Helvetica-Bold", 12)
        c.drawString(2*cm, y, "APPOINTMENT DETAILS")
        y -= 0.7*cm
        
        c.setFont("Helvetica", 10)
        appointment_fields = [
            ("Date:", data.get('appointment_date', 'N/A')),
            ("Time:", data.get('appointment_time', 'N/A')),
            ("Service Type:", data.get('service_type', 'N/A')),
            ("Status:", data.get('status', 'N/A')),
        ]
        
        for label, value in appointment_fields:
            c.drawString(2.5*cm, y, label)
            c.drawString(6*cm, y, str(value))
            y -= 0.6*cm
        
        # Description/Notes
        if data.get('description'):
            y -= 0.5*cm
            c.setFont("Helvetica-Bold", 12)
            c.drawString(2*cm, y, "DESCRIPTION/NOTES")
            y -= 0.7*cm
            
            c.setFont("Helvetica", 10)
            # Wrap text if too long
            description = str(data.get('description', ''))
            max_width = self.page_width - 4*cm
            words = description.split()
            lines = []
            current_line = []
            
            for word in words:
                current_line.append(word)
                text = ' '.join(current_line)
                if c.stringWidth(text, "Helvetica", 10) > max_width:
                    current_line.pop()
                    lines.append(' '.join(current_line))
                    current_line = [word]
            
            if current_line:
                lines.append(' '.join(current_line))
            
            for line in lines:
                c.drawString(2.5*cm, y, line)
                y -= 0.6*cm
        
        return y
    
    def _draw_footer(self, c):
        """Draw PDF footer"""
        c.setFont("Helvetica", 8)
        footer_text = "Auto Servis - Professional Car Service"
        c.drawString(2*cm, 2*cm, footer_text)
        
        page_number = f"Page 1"
        c.drawRightString(self.page_width - 2*cm, 2*cm, page_number)
    
    def print_pdf(self, filepath):
        """
        Print PDF file using system default printer
        
        Args:
            filepath (str): Path to PDF file to print
            
        Returns:
            bool: True if print successful, False otherwise
        """
        if not os.path.exists(filepath):
            print(f"Error: File not found: {filepath}")
            return False
        
        system = platform.system()
        
        try:
            if system == "Windows":
                return self._print_windows(filepath)
            elif system == "Linux":
                return self._print_linux(filepath)
            elif system == "Darwin":  # macOS
                return self._print_macos(filepath)
            else:
                print(f"Unsupported operating system: {system}")
                return False
        except Exception as e:
            print(f"Print error: {e}")
            return False
    
    def _print_windows(self, filepath):
        """Print on Windows using win32print"""
        try:
            import win32print
            import win32api
            
            # Get default printer
            printer_name = win32print.GetDefaultPrinter()
            
            # Print using ShellExecute
            win32api.ShellExecute(
                0,
                "print",
                filepath,
                f'/d:"{printer_name}"',
                ".",
                0
            )
            
            print(f"Printing to: {printer_name}")
            return True
            
        except ImportError:
            print("win32print not available, using alternative method")
            # Alternative method using os.startfile
            try:
                os.startfile(filepath, "print")
                return True
            except Exception as e:
                print(f"Alternative print method failed: {e}")
                return False
        except Exception as e:
            print(f"Windows print error: {e}")
            return False
    
    def _print_linux(self, filepath):
        """Print on Linux using lp command"""
        try:
            import subprocess
            result = subprocess.run(
                ["lp", filepath],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                print("Print job submitted successfully")
                return True
            else:
                print(f"Print error: {result.stderr}")
                return False
                
        except FileNotFoundError:
            print("lp command not found. Install CUPS printing system.")
            return False
        except Exception as e:
            print(f"Linux print error: {e}")
            return False
    
    def _print_macos(self, filepath):
        """Print on macOS using lpr command"""
        try:
            import subprocess
            result = subprocess.run(
                ["lpr", filepath],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                print("Print job submitted successfully")
                return True
            else:
                print(f"Print error: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"macOS print error: {e}")
            return False
    
    def generate_and_print(self, appointment_data, filename=None):
        """
        Generate PDF and immediately print it
        
        Args:
            appointment_data (dict): Appointment data
            filename (str): Optional filename
            
        Returns:
            tuple: (filepath, print_success)
        """
        filepath = self.generate_appointment_pdf(appointment_data, filename)
        print_success = self.print_pdf(filepath)
        return filepath, print_success


# Example usage
if __name__ == "__main__":
    # Test data
    test_appointment = {
        'customer_name': 'John Doe',
        'phone': '+123456789',
        'email': 'john@example.com',
        'vehicle': 'Toyota Camry 2020',
        'license_plate': 'ABC-123',
        'appointment_date': '2026-02-25',
        'appointment_time': '14:00',
        'service_type': 'Regular Maintenance',
        'status': 'Confirmed',
        'description': 'Oil change, tire rotation, and general inspection. Customer mentioned unusual noise from front left wheel.'
    }
    
    # Create printer instance
    printer = AppointmentPrinter()
    
    # Generate PDF
    pdf_path = printer.generate_appointment_pdf(test_appointment)
    print(f"PDF generated: {pdf_path}")
    
    # Optionally print
    if len(sys.argv) > 1 and sys.argv[1] == "--print":
        print("Attempting to print...")
        printer.print_pdf(pdf_path)
