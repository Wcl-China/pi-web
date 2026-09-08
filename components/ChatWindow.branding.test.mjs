import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import test from "node:test";

const source = await readFile(new URL("./ChatWindow.tsx", import.meta.url), "utf8");

test("new chat header uses the Jiyun cloud mark and greeting", () => {
  assert.match(source, /src="\/icons\/jiyun-mark\.svg"/);
  assert.match(source, />你好 jiyun<\/span>/);
  assert.doesNotMatch(source, />π<\/span>/);
  assert.match(source, /NEXT_PUBLIC_APP_VERSION/);
  assert.match(source, /NEXT_PUBLIC_JIYUN_VERSION/);
});
