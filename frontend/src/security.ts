const LOCAL_SOURCE = /^\/demo\/source\/[a-z0-9-]{3,40}$/;

export function safeLocalLink(value: string): string | null {
  return LOCAL_SOURCE.test(value) ? value : null;
}
