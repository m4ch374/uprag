import React, { ReactNode } from "react";
import { Book, Bot, ChevronsUpDown } from "lucide-react";
import { UserButton, useUser } from "@clerk/clerk-react";

const NavBarItem: React.FC<{ children: ReactNode; href: string }> = ({
  children,
  href,
}) => {
  return (
    <a
      className="font-semibold flex gap-2 items-center text-neutral-700 cursor-pointer"
      href={href}
    >
      {children}
    </a>
  );
};

const NavBar: React.FC = () => {
  const { user } = useUser();

  return (
    <div className="flex flex-col justify-between pt-4 h-full min-w-64">
      <div className="flex flex-col">
        <h1 className="text-center text-2xl font-bold">Uprag</h1>
        <ul className="flex flex-col mt-4 w-full px-4 gap-2">
          <NavBarItem href="/chat">
            <Bot />
            Chat
          </NavBarItem>
          <NavBarItem href="/knowledge">
            <Book />
            Knowledge
          </NavBarItem>
        </ul>
      </div>
      <div
        className="my-8 mx-2 justify-between flex bg-white px-4 py-2.5 items-center border border-neutral-200 rounded-sm drop-shadow-md"
        onClick={() => {
          (
            document.querySelector(".cl-userButtonTrigger") as HTMLLIElement
          )?.click();
        }}
      >
        <div className="flex gap-3 items-center">
          <UserButton />
          <h3 className="font-thin">{user?.firstName || "Guest"}</h3>
        </div>
        <ChevronsUpDown className="size-4" />
      </div>
    </div>
  );
};

export default NavBar;
