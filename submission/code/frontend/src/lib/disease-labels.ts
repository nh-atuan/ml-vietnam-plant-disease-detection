const DISEASE_LABELS: Record<string, string> = {
  Healthy: "Cây khỏe mạnh",
  BrownSpot: "Bệnh đốm nâu hại lúa",
  Hispa: "Sâu gai hại lúa",
  LeafBlast: "Bệnh đạo ôn lá lúa",
  LeafMiner: "Sâu vẽ bùa trên lá cà phê",
  PowderyMildew: "Bệnh phấn trắng trên cà phê",
  Rust: "Bệnh gỉ sắt cà phê",
  AlgalLeafSpot: "Bệnh đốm rong trên cà phê",
};

export function getDiseaseDisplayName(label: string) {
  return DISEASE_LABELS[label] ?? "Nhãn bệnh chưa có tên hiển thị";
}
