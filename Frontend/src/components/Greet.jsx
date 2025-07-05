import { useState } from "react";

function ParentComponent() {
  const [valueA, setValueA] = useState("Initial A");
  const [valueB, setValueB] = useState("Initial B");

  const handleClick = () => {
    setValueA("Updated A");
    setValueB("Updated from A");
    // Keep any other logic inside this function
  };

  return (
    <div>
      <ComponentA onButtonClick={handleClick} valueA={valueA} />
      <ComponentB valueB={valueB} />
    </div>
  );
}

function ComponentA({ onButtonClick, valueA }) {
  return (
    <div>
      <p>Value A: {valueA}</p>
      <button onClick={onButtonClick}>Update Both</button>
    </div>
  );
}

function ComponentB({ valueB }) {
  return <div>Value in B: {valueB}</div>;
}

export default ParentComponent;
