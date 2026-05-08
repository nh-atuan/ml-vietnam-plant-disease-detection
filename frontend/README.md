# Frontend — Plant Disease Detection Web App

**Phụ trách:** Dương Tuấn Anh  
**Phase:** 5, Task 5.3

## Stack
- Next.js + Tailwind CSS
- Mobile-first responsive design

## Chức năng chính
1. **Upload ảnh** lá cây (drag & drop hoặc chọn file / chụp camera)
2. **Hiển thị kết quả** chẩn đoán:
   - Nhãn bệnh (tiếng Việt)
   - Độ tin cậy (confidence %)
   - Top-k dự đoán khác
3. **Gợi ý xử lý** bệnh từ Knowledge Base
4. **Lịch sử** chẩn đoán gần đây

## Khởi tạo project
```bash
npx -y create-next-app@latest ./ --typescript --tailwind --eslint --app --src-dir
```

## API endpoint
```
POST /api/v1/predict
Content-Type: multipart/form-data
Body: file (image)

Response: PredictionResponse (xem backend/app/models/schemas.py)
```

## TODO
- [ ] Khởi tạo Next.js project
- [ ] Thiết kế UI/UX (Figma hoặc wireframe)
- [ ] Component: ImageUploader (drag & drop + camera)
- [ ] Component: PredictionResult (hiển thị kết quả)
- [ ] Component: DiseaseInfo (gợi ý xử lý)
- [ ] Component: HistoryList (lịch sử chẩn đoán)
- [ ] Responsive layout (mobile-first)
- [ ] Kết nối API backend
- [ ] Dockerfile cho frontend
