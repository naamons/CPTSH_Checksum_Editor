import streamlit as st
import crcmod
import binascii

# Function to calculate CRC-16 checksum for a given data and polynomial
def calculate_crc16(data, polynomial):
    crc16_func = crcmod.mkCrcFun(polynomial)
    return crc16_func(data)

# Function to update the checksum in the file
def correct_checksum(data, start_address, end_address, checksum_address, polynomial):
    checksum_area = data[start_address:end_address + 1]
    calculated_crc16 = calculate_crc16(checksum_area, polynomial)
    
    # Assuming checksum is stored as 2 bytes (big-endian) at the checksum_address
    corrected_data = bytearray(data)
    corrected_data[checksum_address:checksum_address + 2] = calculated_crc16.to_bytes(2, byteorder='big')
    
    return corrected_data, calculated_crc16

# Streamlit UI
st.title("CRC-16 Checksum Corrector")

# File upload
modified_file = st.file_uploader("Upload the Modified Binary File", type=['bin'])

# Polynomial selection
polynomial = st.selectbox("Select CRC-16 Polynomial", 
                          [("CRC-16-IBM (0x8005)", 0x18005), 
                           ("CRC-16-CCITT (0x1021)", 0x11021)],
                          format_func=lambda x: x[0])

# Address input
start_address = st.number_input("Start Address (Hex)", value=0x1280, format="0x%X")
end_address = st.number_input("End Address (Hex)", value=0xBFD5E, format="0x%X")
checksum_address = st.number_input("Checksum Address (Hex)", value=0xBFD5F, format="0x%X")

if modified_file:
    # Read the binary data
    modified_data = modified_file.read()

    # Correct the checksum in the modified file
    corrected_data, calculated_crc16 = correct_checksum(modified_data, start_address, end_address, checksum_address, polynomial[1])

    # Display the calculated checksum
    st.subheader("Calculated CRC-16 Checksum")
    st.text(f"CRC-16 Checksum: 0x{calculated_crc16:04X}")

    # Provide download link for corrected file
    st.download_button("Download Corrected File", corrected_data, file_name="Corrected_File.bin")

else:
    st.info("Please upload the modified binary file.")
