const GradientBtn = ({ text, onClick = null }) => {
  const buttonStyle = {
    border: 'none',
    padding: '10px 20px',
    borderRadius: '5px',
    cursor: 'pointer',
  };

  return (
    <button onClick={onClick} style={buttonStyle} className="hover:opacity-75 bg-custom-gradient text-white dark:text-light-dark-background">
      {text}
    </button>
  );
};

export default GradientBtn;