'use client'
import SideBar from "../../components/common/SideBar";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
export default function RootLayout({ children }) {
  const [error, setError] = useState(null);
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
    <div className="p-4 sm:ml-[20rem]">
      <SideBar />
      {children}
    </div>
  );
}
