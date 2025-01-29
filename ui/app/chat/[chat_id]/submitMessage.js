import axios from "axios";

const sendMessage = async (chat_id, user_message, token) => {
  try {
    const url = `http://localhost:8000/chats/${chat_id}/message`;

    const response = await axios.post(
      url, // URL with the chat ID
      {}, // Empty body (not required here)
      {
        headers: {
          Authorization: `Bearer ${token}`, // Include token for authentication
        },
        params: {
          user_message, // Pass `user_message` as a query parameter
        },
      }
    );

    return response.data;
  } catch (error) {
    console.error("Error sending message:", error.response?.data || error.message);
    throw error;
  }
};

export default sendMessage;