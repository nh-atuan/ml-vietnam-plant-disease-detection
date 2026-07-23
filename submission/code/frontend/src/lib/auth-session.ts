export const AUTH_SESSION_EXPIRED_EVENT = "plant-disease:session-expired";
export const SESSION_EXPIRED_MESSAGE = "Phiên đăng nhập đã hết hạn. Vui lòng đăng nhập lại.";

export type SessionExpiredDetail = {
  token: string;
};

export function notifySessionExpired(token: string) {
  if (typeof window !== "undefined") {
    window.dispatchEvent(new CustomEvent<SessionExpiredDetail>(AUTH_SESSION_EXPIRED_EVENT, {
      detail: { token },
    }));
  }
}
