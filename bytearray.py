mes = "HKMU"
data = bytearray(mes, "utf-8")
for i in range(len(data)):
    data[i] = data[i] + 4
print("Encrypted:", data)
for i in range(len(data)):
    data[i] = data[i] - 4
print("Decrypted:", data.decode("utf-8"))

