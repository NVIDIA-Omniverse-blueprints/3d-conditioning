-- Shared build scripts from repo_build package
repo_build = require("omni/repo/build")

-- Repo root
root = repo_build.get_abs_path(".")

repo_build.setup_options()
-- Set variables so repo_kit_tools does not set default values for MSVC and WINSDK
MSVC_VERSION = _OPTIONS["visual-cxx-version"]
WINSDK_VERSION = _OPTIONS["winsdk-version"]

kit = require("_repo/deps/repo_kit_tools/kit-template/premake5-kit")
kit.setup_all()

define_app("omni.app.conditioning_for_precise_visual_generative_ai")
define_app("omni.app.conditioning_for_precise_visual_generative_ai_desktop")
define_app("omni.app.conditioning_for_precise_visual_generative_ai_streaming")
