class PlayFairCipher:

    def __init__(self):
        pass

    # ==========================================
    # TẠO MA TRẬN PLAYFAIR
    # ==========================================
    def create_playfair_matrix(self, key):

        key = key.upper()
        key = key.replace("J", "I")
        key = key.replace(" ", "")

        matrix = []
        used = set()

        # Thêm key
        for char in key:

            if char.isalpha() and char not in used:
                used.add(char)
                matrix.append(char)

        # Thêm alphabet còn lại (không có J)
        for char in "ABCDEFGHIKLMNOPQRSTUVWXYZ":

            if char not in used:
                used.add(char)
                matrix.append(char)

        # Chia thành ma trận 5x5
        playfair_matrix = [
            matrix[i:i + 5]
            for i in range(0, 25, 5)
        ]

        return playfair_matrix

    # ==========================================
    # TÌM TỌA ĐỘ KÝ TỰ
    # ==========================================
    def find_letter_coords(self, matrix, letter):

        for row in range(5):

            for col in range(5):

                if matrix[row][col] == letter:
                    return row, col

        return None

    # ==========================================
    # MÃ HÓA PLAYFAIR
    # ==========================================
    def playfair_encrypt(self, plain_text, matrix):

        # Chuẩn hóa dữ liệu
        plain_text = plain_text.upper()
        plain_text = plain_text.replace("J", "I")
        plain_text = plain_text.replace(" ", "")

        # Chỉ giữ chữ cái
        plain_text = ''.join(
            char for char in plain_text
            if char.isalpha()
        )

        encrypted_text = ""

        i = 0

        while i < len(plain_text):

            char1 = plain_text[i]

            # Nếu còn ký tự tiếp theo
            if i + 1 < len(plain_text):

                char2 = plain_text[i + 1]

                # Nếu 2 ký tự giống nhau -> thêm X
                if char1 == char2:

                    pair = char1 + "X"
                    i += 1

                else:

                    pair = char1 + char2
                    i += 2

            else:

                # Nếu lẻ ký tự
                pair = char1 + "X"
                i += 1

            coords1 = self.find_letter_coords(matrix, pair[0])
            coords2 = self.find_letter_coords(matrix, pair[1])

            if coords1 is None or coords2 is None:
                return "Invalid character in text"

            row1, col1 = coords1
            row2, col2 = coords2

            # Cùng hàng
            if row1 == row2:

                encrypted_text += (
                    matrix[row1][(col1 + 1) % 5] +
                    matrix[row2][(col2 + 1) % 5]
                )

            # Cùng cột
            elif col1 == col2:

                encrypted_text += (
                    matrix[(row1 + 1) % 5][col1] +
                    matrix[(row2 + 1) % 5][col2]
                )

            # Hình chữ nhật
            else:

                encrypted_text += (
                    matrix[row1][col2] +
                    matrix[row2][col1]
                )

        return encrypted_text

    # ==========================================
    # GIẢI MÃ PLAYFAIR
    # ==========================================
    def playfair_decrypt(self, cipher_text, matrix):

        cipher_text = cipher_text.upper()
        cipher_text = cipher_text.replace(" ", "")

        decrypted_text = ""

        for i in range(0, len(cipher_text), 2):

            pair = cipher_text[i:i + 2]

            coords1 = self.find_letter_coords(matrix, pair[0])
            coords2 = self.find_letter_coords(matrix, pair[1])

            if coords1 is None or coords2 is None:
                return "Invalid character in cipher text"

            row1, col1 = coords1
            row2, col2 = coords2

            # Cùng hàng
            if row1 == row2:

                decrypted_text += (
                    matrix[row1][(col1 - 1) % 5] +
                    matrix[row2][(col2 - 1) % 5]
                )

            # Cùng cột
            elif col1 == col2:

                decrypted_text += (
                    matrix[(row1 - 1) % 5][col1] +
                    matrix[(row2 - 1) % 5][col2]
                )

            # Hình chữ nhật
            else:

                decrypted_text += (
                    matrix[row1][col2] +
                    matrix[row2][col1]
                )

        # ==========================================
        # LOẠI BỎ X ĐƯỢC THÊM VÀO
        # ==========================================

        banro = ""

        i = 0

        while i < len(decrypted_text):

            # Nếu có dạng AXA -> bỏ X ở giữa
            if (
                i + 2 < len(decrypted_text)
                and decrypted_text[i] == decrypted_text[i + 2]
                and decrypted_text[i + 1] == "X"
            ):

                banro += decrypted_text[i]
                i += 2

            else:

                banro += decrypted_text[i]
                i += 1

        # Nếu X cuối cùng là ký tự thêm vào
        if banro.endswith("X"):

            banro = banro[:-1]

        return banro