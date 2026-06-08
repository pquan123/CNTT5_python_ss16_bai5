er_patients = [
    "ER01|Nguyen Van Quan|HR:115|TEMP:39.5",
    "ER02|Tran Thi Binh|HR:80|TEMP:37.0",
    "ER03|Le Van Cuong|HR:130|TEMP:38.2"
]


def find_patient_index(patients, er_id):
    for index, patient in enumerate(patients):
        if patient.startswith(er_id + "|"):
            return index
    return -1


def extract_vital_value(vital_string):
    return float(vital_string.split(":")[1])


def is_positive_number(value):
    return value.replace(".", "", 1).isdigit() and float(value) > 0


def display_dashboard(patients):
    if not patients:
        print("Khoa cấp cứu hiện đang trống.")
        return

    print("\n--- BẢNG THEO DÕI CA CẤP CỨU ------------------------------------")

    for index, patient in enumerate(patients, start=1):
        er_id, name, hr, temp = patient.split("|")

        hr_value = hr.split(":")[1]
        temp_value = temp.split(":")[1]

        print(
            f"{index}. [{er_id}] {name:<20} | "
            f"Nhịp tim: {hr_value} bpm | "
            f"Nhiệt độ: {temp_value} °C"
        )

    print("-----------------------------------------------------------------")


def admit_patient(patients):
    print("\n--- TIẾP NHẬN CA CẤP CỨU MỚI ---")

    while True:
        er_id = input("Nhập mã ER: ").strip().upper()

        if not er_id:
            print("Mã ER không được để trống!")
            continue

        if find_patient_index(patients, er_id) != -1:
            print("\nMã ca cấp cứu đã tồn tại!")
            return

        break

    while True:
        name = input("Nhập tên bệnh nhân: ").strip()

        if not name:
            print("\nTên bệnh nhân không được để trống!")
            continue

        name = name.title()
        break

    while True:
        hr = input("Nhập nhịp tim HR: ").strip()

        if not is_positive_number(hr):
            print("Sinh hiệu không hợp lệ, vui lòng nhập số lớn hơn 0!")
            continue

        break

    while True:
        temp = input("Nhập nhiệt độ TEMP: ").strip()

        if (
            not temp.replace(".", "", 1).isdigit()
            or float(temp) < 36.5
        ):
            print(
                "Sinh hiệu không hợp lệ, vui lòng nhập số lớn hơn hoặc bằng 36.5!"
            )
            continue

        break

    new_patient = "|".join(
        [
            er_id,
            name,
            f"HR:{int(float(hr))}",
            f"TEMP:{float(temp)}"
        ]
    )

    patients.append(new_patient)

    print("\nTiếp nhận ca cấp cứu mới thành công!")
    print("Sau khi chuẩn hóa, dữ liệu được lưu là:")
    print(new_patient)


def update_vitals(patients):
    print("\n--- CẬP NHẬT LẠI SINH HIỆU ---")

    er_id = input(
        "Nhập mã ER cần cập nhật: "
    ).strip().upper()

    index = find_patient_index(patients, er_id)

    if index == -1:
        print(
            "Không tìm thấy bệnh nhân. Vui lòng kiểm tra lại mã ER!"
        )
        return

    patient_info = patients[index].split("|")

    print(f"Tìm thấy bệnh nhân: {patient_info[1]}")
    print(
        f"Sinh hiệu hiện tại: {patient_info[2]} | {patient_info[3]}"
    )

    print("Bạn muốn cập nhật:")
    print("1. Nhịp tim HR")
    print("2. Nhiệt độ TEMP")

    choice = input("Chọn loại sinh hiệu: ").strip()

    if choice == "1":
        hr = input("Nhập nhịp tim mới: ").strip()

        if not is_positive_number(hr):
            print(
                "\nSinh hiệu không hợp lệ, vui lòng nhập số lớn hơn 0!"
            )
            return

        patient_info[2] = f"HR:{int(float(hr))}"

        patients[index] = "|".join(patient_info)

        print("\nCập nhật nhịp tim thành công!")

    elif choice == "2":
        temp = input("Nhập nhiệt độ mới: ").strip()

        if (
            not temp.replace(".", "", 1).isdigit()
            or float(temp) < 36.5
        ):
            print(
                "\nSinh hiệu không hợp lệ, vui lòng nhập số lớn hơn hoặc bằng 36.5!"
            )
            return

        patient_info[3] = f"TEMP:{float(temp)}"

        patients[index] = "|".join(patient_info)

        print("\nCập nhật nhiệt độ thành công!")

    else:
        print(
            "\nLựa chọn không hợp lệ. Vui lòng chọn 1 hoặc 2!"
        )


def trigger_red_alert(patients):
    if not patients:
        print("Khoa cấp cứu hiện đang trống.")
        return

    critical_count = 0

    print(
        "\n!!! BÁO ĐỘNG ĐỎ - DANH SÁCH BỆNH NHÂN NGUY KỊCH !!!"
    )

    for patient in patients:
        er_id, name, hr, temp = patient.split("|")

        hr_value = extract_vital_value(hr)
        temp_value = extract_vital_value(temp)

        if hr_value > 100 or temp_value >= 39:
            critical_count += 1

            print(
                f"{critical_count}. [{er_id}] "
                f"{name:<20} | "
                f"HR: {int(hr_value)} bpm | "
                f"TEMP: {temp_value} °C | "
                f"CẦN XỬ LÝ KHẨN CẤP"
            )

    if critical_count == 0:
        print(
            "\n--- KIỂM TRA BÁO ĐỘNG ĐỎ ---"
        )
        print(
            "Không có bệnh nhân nguy kịch tại thời điểm hiện tại."
        )
        return

    print("-----------------------------------------------------")
    print(f"Tổng số ca nguy kịch: {critical_count}")


def discharge_patient(patients):
    print("\n--- XUẤT VIỆN / CHUYỂN KHOA ---")

    er_id = input(
        "Nhập mã ER cần xóa khỏi hệ thống: "
    ).strip().upper()

    if not er_id:
        print("Mã ER không được để trống!")
        return

    index = find_patient_index(patients, er_id)

    if index == -1:
        print(
            "Không tìm thấy bệnh nhân. Vui lòng kiểm tra lại mã ER!"
        )
        return

    patient_name = patients[index].split("|")[1]

    patients.pop(index)

    print(
        f"Đã chuyển khoa thành công cho bệnh nhân {patient_name}!"
    )


def display_menu():
    print("\n===== HỆ THỐNG QUẢN LÝ CẤP CỨU RIKKEI ER =====")
    print("1. Bảng theo dõi bệnh nhân")
    print("2. Tiếp nhận ca cấp cứu mới")
    print("3. Cập nhật lại sinh hiệu")
    print("4. BÁO ĐỘNG ĐỎ Lọc bệnh nhân nguy kịch")
    print("5. Xuất viện / Chuyển khoa")
    print("6. Thoát chương trình")
    print("=================================================")


def main():
    while True:
        display_menu()

        choice = input(
            "Chọn chức năng (1-6): "
        ).strip()

        if choice == "1":
            display_dashboard(er_patients)

        elif choice == "2":
            admit_patient(er_patients)

        elif choice == "3":
            update_vitals(er_patients)

        elif choice == "4":
            trigger_red_alert(er_patients)

        elif choice == "5":
            discharge_patient(er_patients)

        elif choice == "6":
            print(
                "\nKết thúc ca trực. Chúc bạn một ngày làm việc hiệu quả!"
            )
            break

        else:
            print("Lựa chọn không hợp lệ!")


main()