import React from "react";
function check() {
  return (
    <>
      <div className="max-w-sm">
        <div className="p-3 flex items-center justify-between border-t cursor-pointer">
          <div className="flex items-center">
            <img
              className="rounded-full h-10 w-10"
              src="https://loremflickr.com/g/600/600/girl"
            />
            <div className="ml-2 flex flex-col">
              <div className="leading-snug text-sm text-white font-bold">
                Jane doe
              </div>
              <div className="leading-snug text-xs text-gray-600">34 posts</div>
            </div>
          </div>
          <button className="h-8 px-3 text-md font-bold text-blue-400 border border-blue-400 rounded-full hover:bg-blue-100">
            Follow
          </button>
        </div>
      </div>

    </>
  );
}

export default check;
