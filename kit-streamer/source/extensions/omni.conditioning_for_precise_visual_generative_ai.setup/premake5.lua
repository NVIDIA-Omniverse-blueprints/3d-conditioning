-- Use folder name to build extension name and tag.
local ext = get_current_extension_info()

project_ext (ext)

-- Link only those files and folders into the extension target directory
repo_build.prebuild_link {
    { "data", ext.target_dir.."/data" },
    { "docs", ext.target_dir.."/docs" },
    { "layouts", ext.target_dir.."/layouts" },
    { "samples", ext.target_dir.."/../../samples" },
    { "omni", ext.target_dir.."/omni" },
}
