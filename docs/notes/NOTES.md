# Ghi chú và lưu ý

## Về báo cáo

- Nên có Danh mục bảng biểu; Danh mục hình vẽ và đồ thị; Bảng thuật ngữ Tiếng Anh - Tiếng Việt; Công thức toán cần được đánh số; Phát biểu định nghĩa hình thức; Có chứng minh ở các mệnh đề nếu cần thiết.
- Không mở ngoặc 1 thuật ngữ tiếng Anh đằng sau 1 thuật ngữ tiếng Việt nếu không phải xuất hiện lần đầu.
- Dấu gạch ngang phải là dấu gạch ngang ngắn - chứ không phải dấu gạch ngang dài.
- Không in đậm/in nghiêng ở các chỗ không cần thiết, đặc biệt là không in đậm ở các từ trước dấu hai chấm của các bullet points.
- Caption của bảng phải nằm ở trên bảng và caption của hình phải nằm phía dưới hình.
- Các bảng không được có đường kẻ dọc, với hàng tiêu đề (header) được in đậm.
- Nên có hình ảnh, sơ đồ minh hoạ.
- Tuyệt đối không được sử dụng ảnh do AI tạo.
- Văn phong: Khoa học, khách quan, súc tích.
- Hình ảnh/Bảng biểu: Mọi hình ảnh, bảng biểu phải được đánh số, có chú thích rõ ràng và được tham chiếu trong nội dung báo cáo.
- Trích dẫn: Trích dẫn đầy đủ các nguồn tài liệu, kiến trúc mô hình tham khảo.
- Giới hạn: Báo cáo không nên vượt quá 30 trang (không bao gồm phụ lục) và khoảng 7000 từ để đảm bảo tính cô đọng.
- Các công thức nếu nằm trong câu chưa kết thúc thì phải có dấu "," ở đằng sau, còn đã kết thúc rồi thì phải có dấu ".".

## Về slides

- Đảm bảo slides cô đọng, có liên quan cũng như có đề cập trong báo cáo.
- Slides phải là tiếng Việt trừ các thuật ngữ tiếng Anh có bản dịch không phổ biến.
- Nên có hình ảnh, sơ đồ minh hoạ.
- Slide đầy đủ nội dung, súc tích, không quá nhiều chữ; có hình ảnh minh hoạ phù hợp.
- Slide chuyên nghiệp, nhất quán về phong cách, dễ đọc.
- Không mở ngoặc 1 thuật ngữ tiếng Anh đằng sau 1 thuật ngữ tiếng Việt nếu không phải xuất hiện lần đầu.
- Hạn chế sử dụng bullet points trong slides
- Không in đậm/in nghiêng ở các chỗ không cần thiết, đặc biệt là không in đậm ở các từ trước dấu hai chấm của các bullet points.
- Dấu gạch ngang phải là dấu gạch ngang ngắn - chứ không phải dấu gạch ngang dài.
- Chỉ sử dụng box cho các công thức toán học hoặc các phần được coi là quan trọng/thú vị. Còn lại không được lạm dụng hay sử dụng quá nhiều.
- Caption của bảng phải nằm ở trên bảng và caption của hình phải nằm phía dưới hình.
- Tiêu đề cột (bên trong columns) nên được căn giữa bằng `\centerline{\textbf{...}}`.
- Các khối văn bản bên dưới tiêu đề cột phải được căn đều hai bên bằng cách chèn `\justifying` trực tiếp trong từng `column` hoặc block.
- Các câu định nghĩa, biểu diễn toán học nên được rút gọn và điều chỉnh cỡ chữ phù hợp (`\small` hoặc `\footnotesize`) để hiển thị trọn vẹn trên một dòng, tránh xuống dòng lẻ loi.
- Hạn chế sử dụng các khối hộp màu (`exampleblock`, `block`) cho các định nghĩa thông thường; thay vào đó nên sử dụng danh sách liệt kê đơn giản (`\item[-]`) không dùng box để slide trông thoáng rộng hơn.
- Sơ đồ tự vẽ (như TikZ) hay hình vẽ minh họa phải được đặt trong môi trường `figure` và có chú thích `\caption{...}` nằm phía dưới hình.
- Màu sắc của các sơ đồ (ví dụ: hình vẽ TikZ) phải đồng bộ với màu chủ đạo của slide (ví dụ: dùng màu thương hiệu `Logo1!10` thay vì `blue!10` mặc định).
- Văn phong trang trọng, học thuật; tránh dùng từ lóng hoặc từ ngữ kém trang trọng.
