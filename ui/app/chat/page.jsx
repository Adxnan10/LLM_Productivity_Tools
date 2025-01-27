"use client";
import useSWR from "swr";
import fetcher from "../../utils/fetcher";
import ChatInputField from "../../components/chat/ChatInputField";
import { useRouter } from "next/navigation";

export default function Home() {
  const router = useRouter(); // Next.js router instance
  const token = localStorage.getItem("token");

  const { data, error, mutate } = useSWR(
    token ? ['http://localhost:8000/chats', token] : null,
    ([url, token]) => fetcher(url, token),
    { revalidateOnFocus: false, shouldRetryOnError: false }
  );

  const handleCreateChat = async (message) => {
    try {
      const newChatData = await mutate();
      router.push(`/chat/${newChatData.chat_id}?initial_message=${message}`); // Redirect to the chat page
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <main className="h-[85vh] sm:h-[90vh]">
      <div className="grid h-full grid-rows-[1fr, auto]">
        <div id="chat-window" className="overflow-y-auto mb-2">
        </div>
      </div>
      <div className="self-end">
        <ChatInputField handleSubmit={handleCreateChat} />
      </div>
    </main>
  );
}
