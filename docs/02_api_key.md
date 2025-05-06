# Preview and Set Up an API Key

*Optional*

>If you do not want to follow a custom workflow and wish to simply run the application, please skip this section and go to [Run the Application](./03_run_app.md)

NIM APIs can be found on the [NVIDIA API Catalog](https://build.nvidia.com/explore/discover).

Follow this example to generate an API key from the API Catalog Preview for the optionally desired NIMs as they appear throughout this guide.

### **Get API Key**

1. Get your NVIDIA API key.
   1. Go to the [NVIDIA API Catalog](https://build.nvidia.com).
   2. Select any model.
   3. Click **Get API Key**.

### **Add API Key**

The following instructions create a temporary environment variable to store your API key. Environment variables set with this method are only stored for a single session. Once a given CMD/PowerShell/Terminal window is closed, these values are  no longer stored.

**Windows CMD**

1. Open Command Prompt.
   1. Enter the following command:
   2. `set NVIDIA_API_KEY="<YOUR_API_KEY>"`
2. Windows PowerShell
   1. Open PowerShell.
   2. Enter the following command:
   3. `$env:NVIDIA_API_KEY="<YOUR_API_KEY>"`

   > [!NOTE]
   > If the two commands above are not working, you can add API key to Windows System Environment Variables.

   Key: `NVIDIA_API_KEY`

   Value: `<YOUR_API_KEY>`

3. Linux Terminal
   1. Open Terminal.
   2. Enter the following command:
      ```
      export NVIDIA_API_KEY="<YOUR_API_KEY>"
      ```

----
<div align="center">
  <table>
    <tr>
      <td align="left"><a href="./01_get_started.md">&larr; Get Started</a></td>
      <td align="center">⠀⠀⠀⠀⠀⠀⠀⠀                    ⠀⠀⠀⠀⠀⠀       </td>
      <td align="right"><a href="./03_run_app.md">Run the Application &rarr;</a></td>
    </tr>
  </table>
</div>
