import org.mozilla.javascript.Context;
import org.mozilla.javascript.Function;
import org.mozilla.javascript.Script;
import org.mozilla.javascript.Scriptable;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Paths;

public class getData {
    public static void main(String[] args) {
        // 创建 Rhino 上下文
        Context cx = Context.enter();
        Scriptable scope = cx.initStandardObjects();

        // 读取 JavaScript 文件内容
        try {
            String scriptPath = "/Users/tanqianqian/Desktop/FYP_web/IoT_website/src/smartContract.js";
            String scriptContent = new String(Files.readAllBytes(Paths.get(scriptPath)), StandardCharsets.UTF_8);

            // 编译 JavaScript 代码
            Script script = cx.compileString(scriptContent, "script", 1, null);

            // 执行 JavaScript 代码
            script.exec(cx, scope);

            // 获取 JavaScript 函数对象
            Object obj = scope.get("getAllMessages", scope);
            if (obj instanceof Function) {
                Function getAllMessages = (Function) obj;

                // 调用 JavaScript 函数
                Object result = getAllMessages.call(cx, scope, scope, new Object[]{});
                System.out.println("All Messages: " + Context.jsToJava(result, Object.class));
            } else {
                System.out.println("Function getAllMessages not found");
            }
        } catch (IOException e) {
            e.printStackTrace();
        } finally {
            // 释放上下文
            Context.exit();
        }
    }
}
