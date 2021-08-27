interface IButton {
  variant?: 'feedback';
  title: string;
  onClick?: () => void;
}

export function Button({title, onClick = () => {}}: IButton) {
  return (
    <button onClick={onClick} onSubmit={onClick}>
      {title}
    </button>
  );
}
