"use client";
import React, { useState, useEffect } from "react";
import { useRouter } from 'next/navigation';

export default function Layout({ children }) {
  const router = useRouter();
  const [error, setError] = useState(null);
  useEffect(() => {
    const token = localStorage.getItem("token");

    if (token) {
      setError("Token found. No need to login");
      return;
    }
  }, []);
  if (error) {
    router.push("/chat");
    return;
  }
  return (
    <>
      {children}
    </>
  );
}
