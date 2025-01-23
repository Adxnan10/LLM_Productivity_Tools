"use client";
import React, { useState } from "react";
import { useRouter } from 'next/navigation';

export default function Page() {
  const router = useRouter();


  const handleSubmit = (e) => {
    e.preventDefault();
    const token = localStorage.getItem("token");
    if (!token) {
      router.push(`/login`);
    } else {
      router.push(`/chat`);
    }
  };

  return (
    <main className="min-h-screen flex flex-col items-center justify-center p-4">
      <div className="content text-center mb-12">
        <h1 className="text-5xl font-extrabold text-transparent bg-clip-text bg-custom-gradient mb-3">
          LLM Productivity tools
        </h1>
        <p className="text-xl text-white italic">AI-powered productivity tools</p>
      </div>

      <form
        onSubmit={handleSubmit}
        className="bg-slate-50 dark:bg-light-dark-background bg-opacity-80 rounded-xl shadow-2xl p-10 max-w-md w-full backdrop-filter backdrop-blur-lg"
      >
        <button
          type="submit"
          className="w-full mt-4 bg-custom-gradient hover:opacity-90 text-white font-bold py-3 px-4 rounded-lg transition duration-300 ease-in-out transform hover:scale-105 focus:outline-none focus:ring-2 focus:ring-[#5976F9] focus:ring-opacity-50"
        >
          Start
        </button>
        <small className="mt-8 text-xs text-center text-gray-400">
          Increase your productivity with AI-driven capabilities
        </small>
      </form>
    </main>
  );
}
