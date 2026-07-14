# Mục lục tài liệu

Thư mục `docs/` được gom theo nhóm để dễ tìm đúng tài liệu theo giai đoạn và mục đích sử dụng.

## Kế hoạch

- [DATA_PLAN.md](plans/DATA_PLAN.md): kế hoạch thu thập, EDA và tiền xử lý dữ liệu.
- [MODEL_PLAN.md](plans/MODEL_PLAN.md): kế hoạch huấn luyện, đánh giá và tinh chỉnh mô hình.
- [WEB_PLAN.md](plans/WEB_PLAN.md): kế hoạch Phase 5-6 cho backend, frontend, API, database và deployment.
- [FINAL_PLAN.md](plans/FINAL_PLAN.md): kế hoạch hoàn thiện báo cáo, slide và demo cuối kỳ.

## Báo cáo

- [ml-proposal.md](reports/ml-proposal.md): đề cương sơ bộ của nhóm.
- [ml-data-report.md](reports/ml-data-report.md): báo cáo dữ liệu đã biên soạn.
- [ml-model-report.md](reports/ml-model-report.md): báo cáo mô hình đã biên soạn.

## API

- [API_DOCUMENTATION.md](api/API_DOCUMENTATION.md): tài liệu endpoint và cách truy cập Swagger/ReDoc.
- [openapi.json](api/openapi.json): đặc tả OpenAPI tĩnh được export từ FastAPI.

## Deploy

- [GCP_K3S_PLAN.md](deployment/GCP_K3S_PLAN.md): kế hoạch đề xuất triển khai Phase 6 bằng 1 VM GCP, k3s, Helm, DuckDNS/Traefik và phối hợp model serving.
- [gcp_setup_guide.md](deployment/gcp_setup_guide.md): hướng dẫn thiết lập hạ tầng GCP, k3s, Helm và DuckDNS cho môi trường triển khai.
- [DEPLOY.md](deployment/DEPLOY.md): runbook deploy lên GCP k3s/Helm.
- **Web App:** `https://plant-disease-demo.duckdns.org`
- **API Docs:** `https://plant-disease-demo.duckdns.org/docs`

## Kiểm thử

- [integration-load-testing.md](testing/integration-load-testing.md): hướng dẫn kiểm thử tích hợp và tải cho API.

## Ghi chú

- [NOTES.md](notes/NOTES.md): ghi chú tổng hợp trong quá trình làm đồ án.
- [MODEL_NOTES.md](notes/MODEL_NOTES.md): ghi chú riêng về mô hình và tài liệu tham khảo.
- [DEVELOPMENT.md](DEVELOPMENT.md): hướng dẫn cài đặt và khởi chạy hệ thống web ở môi trường phát triển cục bộ.

## Yêu cầu đề bài

- [ml-project.md](requirements/ml-project.md): yêu cầu tổng quan của đồ án môn học.
- [ml-data.md](requirements/ml-data.md): khung yêu cầu báo cáo dữ liệu.
- [ml-model.md](requirements/ml-model.md): khung yêu cầu báo cáo mô hình.
- [ml-final-report.md](requirements/ml-final-report.md): khung cấu trúc và nội dung cần có cho báo cáo cuối kỳ.
