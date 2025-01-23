"use client";
import { useState, useEffect } from "react";
import SideBarItem from "./SideBarItem";
import StatIndicator from "./StatIndicator";
import GradientBtn from "../buttons/GradientBtn";
import SideBarBtn from "../buttons/SideBarBtn";
import { FiMoon, FiSun, FiSettings } from "react-icons/fi";
import { BsChatLeftTextFill } from "react-icons/bs";
import { useTheme } from "../../hooks/ThemeContext";
import Image from "next/image";
import { useModelContext } from "../../hooks/ModelContext";
import ModelStatus from "./ModelStatus";

function SideBar() {
  const [showSidebar, setShowSidebar] = useState(true);
  const [showCommands, setShowCommands] = useState(false);
  const { theme, toggleTheme } = useTheme();
  const toggleSidebar = () => setShowSidebar(!showSidebar);
  const {
    modelStatus,
    setModelStatus,
  } = useModelContext();

  return (
    <div>
      <button
        onClick={toggleSidebar}
        data-drawer-target="separator-sidebar"
        data-drawer-toggle="separator-sidebar"
        aria-controls="separator-sidebar"
        type="button"
        className="inline-flex items-center p-2 mt-2 ms-3 text-sm text-gray-500 rounded-lg sm:hidden hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-gray-200 dark:text-gray-400 dark:hover:bg-gray-700 dark:focus:ring-gray-600"
      >
        <span className="sr-only">Open sidebar</span>
        <svg
          className="w-6 h-6"
          aria-hidden="true"
          fill="currentColor"
          viewBox="0 0 20 20"
          xmlns="http://www.w3.org/2000/svg"
        >
          <path
            clipRule="evenodd"
            fillRule="evenodd"
            d="M2 4.75A.75.75 0 012.75 4h14.5a.75.75 0 010 1.5H2.75A.75.75 0 012 4.75zm0 10.5a.75.75 0 01.75-.75h7.5a.75.75 0 010 1.5h-7.5a.75.75 0 01-.75-.75zM2 10a.75.75 0 01.75-.75h14.5a.75.75 0 010 1.5H2.75A.75.75 0 012 10z"
          />
        </svg>
      </button>

      {showSidebar && (
        <aside
          id="separator-sidebar"
          className="fixed top-0 left-0 z-40 w-[20rem] h-screen transition-transform -translate-x-full sm:translate-x-0"
          aria-label="Sidebar"
        >
          <div className="h-full px-3 py-4 overflow-y-auto bg-[#F1F4FA] dark:bg-dark-background border-r border-gray-200 dark:border-light-dark-background">
            {/* close button */}
            {/* <div className='w-full text-left '>
            <button
              onClick={toggleSidebar}
              type="button"
              className="sm:hidden rounded-md text-white bg-gray-200 dark:bg-gray-700 aspect-square"
            >x</button>
          </div> */}
            <ul className="space-y-2 font-medium">
              <li className="logo ">
                <Image
                  src="/logo.png"
                  alt="logo"
                  width={0}
                  height={0}
                  sizes="100vw"
                  style={{ width: "50%", height: "auto" }}
                />
              </li>
              <li className="flex">
                <SideBarItem
                  text={"Model status: "}
                  icon={""}
                  className="text-nowrap m-0"
                />
                <span className="">
                  <ModelStatus status={modelStatus} />
                </span>
              </li>
            </ul>

            <ul className="pt-4 mt-4 space-y-2 max-h-96 overflow-auto font-medium border-t border-gray-200 dark:border-gray-700">
              <li className="text-center">
                <GradientBtn text={"+ New Chat"} />
              </li>
              <li>
                <SideBarItem
                  text={`Dummy Chat 11`}
                  active={true}
                  icon={<BsChatLeftTextFill />}
                />
                {[1, 2, 3, 4, 5, 6, 7, 8, 9, 10].reverse().map((i) => {
                  return (
                    <SideBarItem
                      key={i}
                      text={`Dummy Chat ${i}`}
                      active={false}
                      icon={<BsChatLeftTextFill />}
                    />
                  );
                })}


              </li>
            </ul>
            {/* The very end of the side bar would contain settings like a button for theme (dark/white), a button for settins (gear shape), and lastly a button to sign in and out which willl be disabled */}
            {/* theme btn */}
            <div className="absolute bottom-5 left-0 right-0 flex space-x-4 items-center justify-center">
              <SideBarBtn
                icon={theme == "dark" ? <FiSun /> : <FiMoon />}
                onClick={toggleTheme}
              />
              <SideBarBtn icon={<FiSettings />} onClick={() => { }} />
              {/* <SideBarBtn
              icon={<FiUser />}
              onClick={() => { }}
              disabled={true}
            /> */}
            </div>
          </div>
        </aside>
      )}
    </div>
  );
}

export default SideBar;
