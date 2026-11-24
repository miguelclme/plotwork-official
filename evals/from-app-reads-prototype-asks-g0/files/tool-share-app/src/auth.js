// Demo sign-in: any email signs in as one of the demo residents. There is no password check.
import { demoResidents } from "./demoData.js";

const KEY = "toolshare.user";

export function signIn(email) {
  const resident = demoResidents.find((r) => r.email === email) ?? demoResidents[0];
  localStorage.setItem(KEY, JSON.stringify(resident));
  return resident;
}

export function signOut() {
  localStorage.removeItem(KEY);
}

export function currentUser() {
  const saved = localStorage.getItem(KEY);
  return saved ? JSON.parse(saved) : null;
}
