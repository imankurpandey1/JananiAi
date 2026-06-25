import React from "react";
import { createRoot } from "react-dom/client";
import { Toaster } from "react-hot-toast";
import App from "./App.jsx";
import "./styles.css";
import { AuthProvider } from "./context/AuthContext.jsx";
import { GoogleOAuthProvider } from "@react-oauth/google";

const GOOGLE_CLIENT_ID = "618003048467-libua714ra4mdbe0tk2qqb915gorovoh.apps.googleusercontent.com";

createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <GoogleOAuthProvider clientId={GOOGLE_CLIENT_ID}>
      <AuthProvider>
        <App />
        <Toaster position="top-right" toastOptions={{ style: { background: "#10231d", color: "#f8fafc", border: "1px solid rgba(16,185,129,.25)" } }} />
      </AuthProvider>
    </GoogleOAuthProvider>
  </React.StrictMode>
);
