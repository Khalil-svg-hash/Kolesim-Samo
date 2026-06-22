import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

const PROTECTED_PATHS = ["/profile", "/constructor"];

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;

  // Only check protected paths - auth state is handled client-side via zustand
  // The middleware just ensures the route group layout loads
  return NextResponse.next();
}

export const config = {
  matcher: ["/((?!api|_next/static|_next/image|favicon.ico).*)"],
};