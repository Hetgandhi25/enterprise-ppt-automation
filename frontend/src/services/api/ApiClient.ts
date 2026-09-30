import { useAuthStore } from "../../stores/useAuthStore";

const API_BASE_URL = "http://localhost:8000/api";

export class ApiClient {
  static async fetch(endpoint: string, options: RequestInit = {}): Promise<Response> {
    const token = useAuthStore.getState().token;
    
    const headers: Record<string, string> = {
      ...(options.headers as Record<string, string> || {})
    };

    if (token) {
      headers["Authorization"] = `Bearer ${token}`;
    }

    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      ...options,
      headers
    });

    if (response.status === 401 || response.status === 403) {
      // If unauthorized/forbidden, maybe auto-logout or let the caller handle
      if (response.status === 401) {
        useAuthStore.getState().logout();
      }
    }

    return response;
  }
}
