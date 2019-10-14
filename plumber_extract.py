import pdfplumber

if __name__ == "__main__":
	file_path = "extract_test.pdf"
	saved_file_path = file_path.split(".")[0] + "_extract" + ".txt"
	pdf = pdfplumber.open(file_path)
	for page in pdf.pages:
		with open(saved_file_path, "a", encoding="utf-8") as f:
			# 按页 顺序写入
			f.write(page.extract_text())
			f.write("\n")
	pdf.close()
