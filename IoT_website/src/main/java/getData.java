// YourJavaFile.java

import javax.script.ScriptEngine;
import javax.script.ScriptEngineManager;
import javax.script.ScriptException;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.nio.charset.StandardCharsets;

public class getData {
    public static void main(String[] args) {
        // 创建 JavaScript 引擎
        ScriptEngineManager manager = new ScriptEngineManager();
        ScriptEngine engine = manager.getEngineByName("javascript");

        // 读取 JavaScript 文件内容
        try {
            String scriptPath = "/Users/tanqianqian/Desktop/FYP_web/IoT_website/src/smartContract.js";
            String scriptContent = new String(Files.readAllBytes(Paths.get(scriptPath)), StandardCharsets.UTF_8);

            //String scriptContent = new String(Files.readAllBytes(Paths.get("smartContract.js")), StandardCharsets.UTF_8);

            // 执行 JavaScript 代码
            engine.eval(scriptContent);

            // 调用 JavaScript 函数
            Object result = engine.eval("getAllMessages()");
            System.out.println("All Messages: " + result);
        } catch (ScriptException | IOException e) {
            e.printStackTrace();
        }
    }
}
