'use client'
import { ThemeProvider } from '../hooks/ThemeContext'; // Adjust the path if necessary
import { ModelProvider } from '../hooks/ModelContext'; // Adjust the import path as necessary
import "../styles/globals.css";

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body
        className={
          "text-[#004aad] dark:text-white bg-[#FFF] dark:bg-dark-background"
        }
      >
        <ThemeProvider>
          <ModelProvider>
            {children}
          </ModelProvider>
        </ThemeProvider>
      </body>
    </html>
  );
}