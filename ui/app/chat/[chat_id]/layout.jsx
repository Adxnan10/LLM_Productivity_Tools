'use client'
import SideBar from "../../../components/common/SideBar";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
export default function RootLayout({ children }) {
  const [error, setError] = useState(null);
  // TODO check if the chat_id is valid and belongs to the user
  const router = useRouter();
  useEffect(() => {
    const token = localStorage.getItem("token");

    if (!token) {
      setError("No token found. Please login first.");
      return;
    }
  }, []);

  if (error) {
    router.push("/auth/login");
    return <div>Error: {error} </div>;
  }

  return (
    <div>
      <SideBar />
      {children}
    </div>
  );
}
