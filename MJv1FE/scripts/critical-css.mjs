import critical from "critical";
import path from "path";

(async () => {
  try {
    await critical.generate({
      base: path.resolve(process.cwd(), "dist"),
      src: "index.html",
      dest: "index.html",
      inline: true,
      minify: true,
      width: 1920,
      height: 1080,
      penthouse: {
        blockJSRequests: false,
      },
    });
    console.log("✅ Critical CSS 提取完成！");
  } catch (err) {
    console.error("❌ Critical CSS 提取失败:", err);
  }
})();