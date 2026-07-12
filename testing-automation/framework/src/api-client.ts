type Credentials = { email: string; password: string; profileType: string };

const safeMessage = (status: number, body: unknown): string => {
  const value = body && typeof body === "object" && "message" in body
    ? String((body as { message: unknown }).message)
    : "Request failed";
  return `API ${status}: ${value.slice(0, 300)}`;
};

export const createApiClient = (baseUrl: string) => {
  const request = async <T>(path: string, init: RequestInit = {}, token?: string): Promise<T> => {
    const headers = new Headers(init.headers);
    headers.set("Accept", "application/json");
    if (token) headers.set("Authorization", `Bearer ${token}`);
    const response = await fetch(`${baseUrl}${path}`, { ...init, headers });
    const body = await response.json().catch(() => null);
    if (!response.ok) throw new Error(safeMessage(response.status, body));
    return body as T;
  };

  return {
    login: async ({ email, password, profileType }: Credentials): Promise<string> => {
      const body = await request<{ token?: string }>("/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password, profile_type: profileType }),
      });
      if (!body.token) throw new Error("Authentication response did not contain a token");
      return body.token;
    },
    get: <T>(path: string, token: string) => request<T>(path, {}, token),
    postJson: <T>(path: string, body: unknown, token: string) => request<T>(path, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }, token),
    postForm: <T>(path: string, body: FormData, token: string) => request<T>(path, { method: "POST", body }, token),
  };
};
