import { PropsWithChildren } from "react";
import NavBar from "./NavBar";

export default function Layout({ children }: PropsWithChildren) {
  return (
    <div className="min-h-screen bg-slate-50">
      <NavBar />
      <main className="py-6">{children}</main>
      <footer className="mt-12 py-8 border-t border-slate-200">
        <div className="container-page text-sm text-slate-500">
          © {new Date().getFullYear()} NFL Parlay Predictor
        </div>
      </footer>
    </div>
  );
}
