
function SideBarItem({ text, icon, link = "#", className = "", active = false }) {
  className += active ? "bg-gray-100 dark:bg-gray-700" : "";
  return (
    <a
      href={link}
      className={"flex items-center p-4 text-gray-900 rounded-lg dark:text-white hover:bg-gray-100 dark:hover:bg-gray-700 " + className}
    >
      {icon}
      <span className="ms-3">{text}</span>
    </a>
  )
}

export default SideBarItem