"use client";
import { useState, useEffect, useRef } from "react";
import useSWR from "swr";
import { usePathname, useSearchParams } from "next/navigation";
import ChatInputField from "../../../components/chat/ChatInputField";
import UserChatBubble from "../../../components/chat/UserChatBubble";
import BotChatBubble from "../../../components/chat/BotChatBubble";
import fetcher from "../../../utils/fetcher";
import sendMessage from "./submitMessage";


// const fetcher = url => axios.post(url).then(res => res.data);
// TODO implement logic for fetching data from the server
// const chain = new RemoteRunnable({
//   url: `http://localhost:8000/graph/`,
// });
const markdownContent = `
  # Hello World
 
  
# h1 Heading 
**This is bold text**
__This is bold text__
*This is italic text*
_This is italic text_
~~Strikethrough~~
  This is a code block:
  \`\`\`cli
  ls
  \`\`\`
  ## Tables
 
  | Syntax | Description |
  | ----------- | ----------- |
  | Header | Title |
  | Paragraph | Text |
  
  `;

export default function Home() {
  const [messages, setMessages] = useState([]);
  const [tempMessages, setTempMessages] = useState([]);
  const searchParams = useSearchParams();
  const pathname = usePathname();
  const token = localStorage.getItem("token");
  const [MessageIsLoading, setIsLoading] = useState(false); // Loading state
  const [MessageError, setError] = useState(null); // Error state
  // get params from the URL
  const initial_message = searchParams.get("initial_message");
  const chat_id = pathname.split("/").pop();
  const initialMessageSent = useRef(false);


  // Fetch messages from API with SWR
  const { data, error: swrError, isLoading } = useSWR(
    chat_id ? `http://localhost:8000/chats/${chat_id}` : null,
    (url) => fetcher(url, token, "GET")
  );


  useEffect(() => {
    if (data) {
      const obj_data = JSON.parse(data);
      setMessages(obj_data);
    }

  }, [data]);

  const handleSendMessage = async (userMessage) => {
    console.log("userMessage", userMessage);
    try {
      setIsLoading(true);

      // Update messages locally with user's message
      const userMessageObject = { message: userMessage, response: "loading" };
      setMessages((prev) => [...prev, userMessageObject]);

      const updated_message_with_response = await sendMessage(chat_id, userMessage, token);
      console.log("updated_message_with_response", updated_message_with_response);
      const obj_updated_message = JSON.parse(updated_message_with_response);
      console.log("obj_updated_message", obj_updated_message);
      // Update messages locally with the bot's response
      setMessages((prev) =>
        prev.map((msg, index) =>
          index === prev.length - 1 ? obj_updated_message : msg
        )
      );

    } catch (err) {
      console.error("Failed to send message:", err);
      setError("Failed to send message.");
    } finally {
      setIsLoading(false);
    }
  };


  useEffect(() => {
    const handleInitialMessage = async () => {
      console.log("handleInitialMessage is called");
      if (isLoading) return;
      if (swrError) return;
      const obj_data = JSON.parse(data);
      console.log("handleInitialMessage has passed the first two checks");
      console.log("initial_message:", initial_message);
      console.log("data length ", obj_data.length);
      console.log("initialMessageSent.current", initialMessageSent.current);
      console.log("initial_message", !initial_message);
      if (!initial_message || obj_data.length || initialMessageSent.current) return;

      console.log("handleSendMessage is called");
      initialMessageSent.current = true; // Mark as sent
      await handleSendMessage(initial_message);
    };

    handleInitialMessage();
  }, [initial_message, data, isLoading, swrError]);


  // scroll to the bottom of the chat window when a new message is added
  useEffect(() => {
    const chatWindow = document.getElementById("chat-window");
    if (chatWindow)
      chatWindow.scrollTop = chatWindow.scrollHeight;
  }, [messages]);

  // Render loading, error, and chat UI
  if (!data && !swrError) return <p>Loading...</p>;
  if (swrError) return <p style={{ color: "red" }}>Error: {swrError.message}</p>;


  return (
    <main className="h-[85vh] sm:h-[90vh]">
      <div className="grid h-full grid-rows-[1fr, auto]">
        <div id="chat-window" className="overflow-y-auto mb-2">
          <div className="flex flex-col gap-3">
            {messages.map((message, index) =>
            (<div key={index}>
              <UserChatBubble key={`user-${index}`}>
                {message.message}
              </UserChatBubble>
              <BotChatBubble
                key={`bot-${index}`}
                bot_name={"LLM"}
              >
                {message.response}
              </BotChatBubble>
            </div>))
            }
          </div>
        </div>
      </div>
      <div className="self-end">
        <ChatInputField handleSubmit={handleSendMessage} />
      </div>
    </main>
  );
}
