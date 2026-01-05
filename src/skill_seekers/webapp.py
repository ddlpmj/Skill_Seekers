"""
Skill Seekers Web Application
A Streamlit-based UI for configuring and running Skill Seekers workflows
"""

import streamlit as st
import json
import os
import sys
from pathlib import Path
import subprocess
from typing import Dict, Optional

# Page configuration
st.set_page_config(
    page_title="Skill Seekers",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .success-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
    }
    .info-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        color: #0c5460;
    }
</style>
""", unsafe_allow_html=True)


def init_session_state():
    """Initialize session state variables"""
    if 'configs' not in st.session_state:
        st.session_state.configs = {}
    if 'current_config' not in st.session_state:
        st.session_state.current_config = None
    if 'scraping_status' not in st.session_state:
        st.session_state.scraping_status = None


def load_existing_configs() -> Dict[str, dict]:
    """Load existing configuration files from configs/ directory"""
    configs_dir = Path("configs")
    configs = {}

    if configs_dir.exists():
        for config_file in configs_dir.glob("*.json"):
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    config_data = json.load(f)
                    configs[config_file.stem] = config_data
            except Exception as e:
                st.warning(f"Failed to load {config_file}: {e}")

    return configs


def save_config(config_name: str, config_data: dict) -> bool:
    """Save configuration to file"""
    try:
        configs_dir = Path("configs")
        configs_dir.mkdir(exist_ok=True)

        config_file = configs_dir / f"{config_name}.json"
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config_data, f, indent=2, ensure_ascii=False)

        return True
    except Exception as e:
        st.error(f"Failed to save config: {e}")
        return False


def page_home():
    """Home page with overview"""
    st.markdown('<h1 class="main-header">🎯 Skill Seekers Web Interface</h1>', unsafe_allow_html=True)

    st.markdown("""
    ### Welcome to Skill Seekers!

    This web interface provides a complete workflow for converting documentation into LLM skills.

    ## 🚀 Features

    - **📝 Configuration Generator**: Create and manage configuration files
    - **🌐 Documentation Scraper**: Scrape documentation websites
    - **📦 Skill Packager**: Package skills for different platforms
    - **☁️ Upload to Platforms**: Upload to Claude AI, Gemini, OpenAI, etc.
    - **🔄 Complete Workflow**: Automate the entire process

    ## 📚 Quick Start

    1. Navigate to **Configuration Generator** to create a config
    2. Use **Documentation Scraper** to scrape the content
    3. Go to **Skill Packager** to package your skill
    4. Use **Upload** to deploy to your preferred platform

    Or use the **Complete Workflow** page for automation!
    """)

    # Statistics
    col1, col2, col3, col4 = st.columns(4)

    configs = load_existing_configs()
    output_dirs = list(Path("output").glob("*")) if Path("output").exists() else []

    with col1:
        st.metric("Available Configs", len(configs))

    with col2:
        st.metric("Output Projects", len(output_dirs))

    with col3:
        st.metric("Supported Platforms", "4")

    with col4:
        st.metric("MCP Tools", "18")


def page_config_generator():
    """Configuration file generator page"""
    st.title("📝 Configuration Generator")

    # Option to load existing or create new
    tab1, tab2 = st.tabs(["Create New Config", "Manage Existing Configs"])

    with tab1:
        st.subheader("Create New Configuration")

        # Basic Information
        col1, col2 = st.columns(2)
        with col1:
            config_name = st.text_input("Configuration Name*", placeholder="my-framework")
        with col2:
            description = st.text_input("Description*", placeholder="When to use this skill")

        base_url = st.text_input("Base URL*", placeholder="https://docs.example.com/")

        # Selectors
        st.subheader("CSS Selectors")
        col1, col2, col3 = st.columns(3)
        with col1:
            main_content = st.text_input("Main Content Selector", value="article, main, .content")
        with col2:
            title_selector = st.text_input("Title Selector", value="h1, .title")
        with col3:
            code_selector = st.text_input("Code Block Selector", value="pre code")

        # URL Patterns
        st.subheader("URL Patterns")
        col1, col2 = st.columns(2)
        with col1:
            include_patterns = st.text_area(
                "Include Patterns (one per line)",
                placeholder="/docs\n/guides\n/api",
                help="Only scrape URLs containing these patterns"
            )
        with col2:
            exclude_patterns = st.text_area(
                "Exclude Patterns (one per line)",
                placeholder="/blog\n/api-reference\n/examples",
                help="Skip URLs containing these patterns"
            )

        # Categories
        st.subheader("Categories")
        categories_text = st.text_area(
            "Categories (JSON format)",
            value="""{
  "getting_started": ["intro", "quickstart", "installation"],
  "api": ["api", "reference"],
  "guides": ["guide", "tutorial"]
}""",
            height=150
        )

        # Advanced Settings
        with st.expander("Advanced Settings"):
            col1, col2, col3 = st.columns(3)
            with col1:
                max_pages = st.number_input("Max Pages", min_value=1, max_value=10000, value=500)
            with col2:
                rate_limit = st.number_input("Rate Limit (seconds)", min_value=0.0, max_value=5.0, value=0.5, step=0.1)
            with col3:
                timeout = st.number_input("Request Timeout (seconds)", min_value=5, max_value=120, value=30)

        # Generate Config
        if st.button("🔧 Generate Configuration", type="primary"):
            if not config_name or not base_url:
                st.error("❌ Configuration Name and Base URL are required!")
                return

            try:
                # Parse categories
                try:
                    categories = json.loads(categories_text) if categories_text else {}
                except json.JSONDecodeError:
                    st.error("❌ Invalid JSON format for categories")
                    return

                # Parse patterns
                include = [p.strip() for p in include_patterns.split('\n') if p.strip()]
                exclude = [p.strip() for p in exclude_patterns.split('\n') if p.strip()]

                # Build config
                config = {
                    "name": config_name,
                    "description": description,
                    "base_url": base_url,
                    "selectors": {
                        "main_content": main_content,
                        "title": title_selector,
                        "code_blocks": code_selector
                    },
                    "url_patterns": {
                        "include": include,
                        "exclude": exclude
                    },
                    "categories": categories,
                    "rate_limit": rate_limit,
                    "max_pages": max_pages,
                    "timeout": timeout
                }

                # Save config
                if save_config(config_name, config):
                    st.success(f"✅ Configuration saved to `configs/{config_name}.json`")

                    # Show preview
                    with st.expander("📄 View Generated Config"):
                        st.json(config)

            except Exception as e:
                st.error(f"❌ Error generating configuration: {e}")

    with tab2:
        st.subheader("Manage Existing Configurations")

        configs = load_existing_configs()

        if not configs:
            st.info("No existing configurations found. Create one in the 'Create New Config' tab.")
        else:
            selected_config = st.selectbox("Select Configuration", list(configs.keys()))

            if selected_config:
                config = configs[selected_config]

                col1, col2 = st.columns([3, 1])

                with col1:
                    st.json(config)

                with col2:
                    st.write("**Actions**")

                    if st.button("📋 Copy to Clipboard", key=f"copy_{selected_config}"):
                        st.code(json.dumps(config, indent=2), language="json")

                    if st.button("🗑️ Delete", key=f"delete_{selected_config}"):
                        config_path = Path(f"configs/{selected_config}.json")
                        if config_path.exists():
                            config_path.unlink()
                            st.success(f"✅ Deleted {selected_config}.json")
                            st.rerun()


def page_scraper():
    """Documentation scraper page"""
    st.title("🌐 Documentation Scraper")

    # Load configs
    configs = load_existing_configs()

    if not configs:
        st.warning("⚠️ No configurations found. Please create one first in the Configuration Generator.")
        return

    # Select config
    col1, col2 = st.columns([2, 1])
    with col1:
        selected_config = st.selectbox("Select Configuration", list(configs.keys()))
    with col2:
        st.write("")
        st.write("")
        config_type = st.selectbox("Config Type", ["Documentation", "GitHub", "PDF", "Unified"])

    if selected_config:
        config = configs[selected_config]
        st.json(config)

        # Options
        col1, col2, col3 = st.columns(3)
        with col1:
            dry_run = st.checkbox("Dry Run (no actual scraping)", value=True)
        with col2:
            async_mode = st.checkbox("Async Mode (faster)", value=False)
        with col3:
            skip_scrape = st.checkbox("Skip Scraping (rebuild only)", value=False)

        # Scrape button
        if st.button("🚀 Start Scraping", type="primary"):
            st.info(f"🔄 Starting to scrape using configuration: {selected_config}")

            # Build command
            cmd = []

            if config_type == "Documentation":
                cmd = ["skill-seekers-scrape", "--config", f"configs/{selected_config}.json"]
            elif config_type == "GitHub":
                cmd = ["skill-seekers-github", "--repo", config.get("repo", ""), "--name", selected_config]
            elif config_type == "PDF":
                cmd = ["skill-seekers-pdf", config.get("pdf_path", "")]
            elif config_type == "Unified":
                cmd = ["skill-seekers-unified", "--config", f"configs/{selected_config}.json"]

            # Add options
            if dry_run:
                cmd.append("--dry-run")
            if async_mode:
                cmd.append("--async")
            if skip_scrape:
                cmd.append("--skip-scrape")

            # Show command
            st.code(" ".join(cmd), language="bash")

            # Run command
            if st.button("⚡ Execute Command", key="execute_scrape"):
                try:
                    result = subprocess.run(
                        cmd,
                        capture_output=True,
                        text=True,
                        timeout=600  # 10 minutes
                    )

                    if result.returncode == 0:
                        st.success("✅ Scraping completed successfully!")
                        with st.expander("📄 View Output"):
                            st.text(result.stdout)
                    else:
                        st.error("❌ Scraping failed!")
                        with st.expander("📄 View Error"):
                            st.text(result.stderr)

                except subprocess.TimeoutExpired:
                    st.error("❌ Command timed out after 10 minutes")
                except Exception as e:
                    st.error(f"❌ Error: {e}")


def page_packager():
    """Skill packager page"""
    st.title("📦 Skill Packager")

    # Check for output directories
    output_dir = Path("output")
    if not output_dir.exists():
        st.warning("⚠️ No output directories found. Please scrape documentation first.")
        return

    # Get output projects
    projects = [d.name for d in output_dir.iterdir() if d.is_dir()]

    if not projects:
        st.warning("⚠️ No projects found in output directory.")
        return

    # Select project
    selected_project = st.selectbox("Select Project", projects)

    if selected_project:
        project_path = output_dir / selected_project

        # Show project info
        st.info(f"📁 Project path: `{project_path}`")

        # Check if SKILL.md exists
        skill_md = project_path / "SKILL.md"
        if skill_md.exists():
            st.success("✅ SKILL.md found")
            with st.expander("📄 Preview SKILL.md (first 50 lines)"):
                with open(skill_md, 'r') as f:
                    lines = f.readlines()[:50]
                st.code("".join(lines), language="markdown")
        else:
            st.warning("⚠️ SKILL.md not found. Please scrape first.")

        # Platform selection
        st.subheader("Packaging Options")
        target_platform = st.selectbox(
            "Target Platform",
            ["claude", "gemini", "openai", "markdown"],
            help="Choose which LLM platform to package for"
        )

        col1, col2 = st.columns(2)
        with col1:
            dry_run = st.checkbox("Dry Run", value=True)
        with col2:
            output_location = st.text_input("Output Path", value="output/")

        # Package button
        if st.button("📦 Package Skill", type="primary"):
            cmd = [
                "skill-seekers-package",
                str(project_path),
                "--target", target_platform
            ]

            if dry_run:
                cmd.append("--dry-run")

            st.code(" ".join(cmd), language="bash")

            if st.button("⚡ Execute Packaging", key="execute_package"):
                try:
                    result = subprocess.run(
                        cmd,
                        capture_output=True,
                        text=True,
                        timeout=60
                    )

                    if result.returncode == 0:
                        st.success(f"✅ Successfully packaged for {target_platform}!")
                        with st.expander("📄 View Output"):
                            st.text(result.stdout)
                    else:
                        st.error("❌ Packaging failed!")
                        with st.expander("📄 View Error"):
                            st.text(result.stderr)

                except subprocess.TimeoutExpired:
                    st.error("❌ Command timed out")
                except Exception as e:
                    st.error(f"❌ Error: {e}")


def page_upload():
    """Upload to platforms page"""
    st.title("☁️ Upload to Platforms")

    # List available packages
    output_dir = Path("output")
    packages = []

    if output_dir.exists():
        packages = list(output_dir.glob("*.zip")) + list(output_dir.glob("*.tar.gz"))

    if not packages:
        st.warning("⚠️ No packages found. Please package a skill first.")
        return

    # Select package
    package_names = [p.name for p in packages]
    selected_package = st.selectbox("Select Package", package_names)

    if selected_package:
        package_path = output_dir / selected_package

        # Detect platform from filename
        if "claude" in selected_package.lower():
            platform = "claude"
        elif "gemini" in selected_package.lower():
            platform = "gemini"
        elif "openai" in selected_package.lower():
            platform = "openai"
        else:
            platform = "markdown"

        st.info(f"🔍 Detected platform: **{platform.upper()}**")

        # API key input
        env_var = {
            "claude": "ANTHROPIC_API_KEY",
            "gemini": "GOOGLE_API_KEY",
            "openai": "OPENAI_API_KEY"
        }.get(platform, "")

        if env_var:
            api_key = st.text_input(
                f"API Key ({env_var})",
                type="password",
                help=f"You can also set this as environment variable: {env_var}"
            )
        else:
            api_key = None

        # Upload button
        if st.button("☁️ Upload Skill", type="primary"):
            cmd = ["skill-seekers-upload", str(package_path), "--target", platform]

            st.code(" ".join(cmd), language="bash")

            if st.button("⚡ Execute Upload", key="execute_upload"):
                try:
                    env = os.environ.copy()
                    if api_key and env_var:
                        env[env_var] = api_key

                    result = subprocess.run(
                        cmd,
                        capture_output=True,
                        text=True,
                        timeout=300,
                        env=env
                    )

                    if result.returncode == 0:
                        st.success(f"✅ Successfully uploaded to {platform.upper()}!")
                        with st.expander("📄 View Output"):
                            st.text(result.stdout)
                    else:
                        st.error("❌ Upload failed!")
                        with st.expander("📄 View Error"):
                            st.text(result.stderr)

                except subprocess.TimeoutExpired:
                    st.error("❌ Command timed out")
                except Exception as e:
                    st.error(f"❌ Error: {e}")


def page_workflow():
    """Complete workflow automation page"""
    st.title("🔄 Complete Workflow Automation")

    st.markdown("""
    This page automates the entire workflow from URL to uploaded skill.

    **Steps:**
    1. 📝 Generate/create configuration
    2. 🌐 Scrape documentation
    3. 🤖 AI Enhancement (optional)
    4. 📦 Package for target platform
    5. ☁️ Upload to platform
    """)

    # Load configs
    configs = load_existing_configs()

    if not configs:
        st.warning("⚠️ No configurations found. Please create one first.")
        return

    # Workflow configuration
    col1, col2 = st.columns(2)
    with col1:
        selected_config = st.selectbox("Select Configuration", list(configs.keys()))
        target_platform = st.selectbox(
            "Target Platform",
            ["claude", "gemini", "openai", "markdown"]
        )
    with col2:
        enable_enhancement = st.checkbox("Enable AI Enhancement", value=False)
        dry_run = st.checkbox("Dry Run ( Entire Workflow)", value=True)

    if selected_config:
        config = configs[selected_config]

        # Workflow summary
        st.subheader("Workflow Summary")
        steps = []
        steps.append(f"1. 📝 Using configuration: {selected_config}")
        steps.append(f"2. 🌐 Scraping: {config.get('base_url', 'N/A')}")
        if enable_enhancement:
            steps.append(f"3. 🤖 AI Enhancement: Enabled (using {target_platform} model)")
        steps.append(f"{'3' if not enable_enhancement else '4'}. 📦 Package for: {target_platform.upper()}")
        steps.append(f"{'4' if not enable_enhancement else '5'}. ☁️ Upload to: {target_platform.upper()}")

        for step in steps:
            st.markdown(f"- {step}")

        # Execute workflow
        if st.button("🚀 Start Complete Workflow", type="primary"):
            st.info("🔄 Starting workflow...")

            # Use install command
            cmd = [
                "skill-seekers-install",
                config.get('base_url', ''),
                "--config", f"configs/{selected_config}.json",
                "--target", target_platform
            ]

            if enable_enhancement:
                cmd.append("--enhance")

            if dry_run:
                cmd.append("--dry-run")

            st.code(" ".join(cmd), language="bash")

            if st.button("⚡ Execute Workflow", key="execute_workflow"):
                try:
                    result = subprocess.run(
                        cmd,
                        capture_output=True,
                        text=True,
                        timeout=1800  # 30 minutes
                    )

                    if result.returncode == 0:
                        st.success("✅ Workflow completed successfully!")
                        with st.expander("📄 View Output"):
                            st.text(result.stdout)
                    else:
                        st.error("❌ Workflow failed!")
                        with st.expander("📄 View Error"):
                            st.text(result.stderr)

                except subprocess.TimeoutExpired:
                    st.error("❌ Workflow timed out after 30 minutes")
                except Exception as e:
                    st.error(f"❌ Error: {e}")


def main():
    """Main application entry point for CLI"""
    import sys
    import subprocess

    # Re-run this script with streamlit
    # This allows the CLI command to work properly
    script_path = Path(__file__).absolute()
    subprocess.run([sys.executable, "-m", "streamlit", "run", str(script_path)])


if __name__ == "__main__":
    # Check if we're being run by streamlit or directly
    import sys
    if "streamlit" in sys.modules:
        # Being run by streamlit, show the UI
        init_session_state()

        # Sidebar navigation
        st.sidebar.title("🎯 Skill Seekers")

        pages = {
            "🏠 Home": page_home,
            "📝 Config Generator": page_config_generator,
            "🌐 Documentation Scraper": page_scraper,
            "📦 Skill Packager": page_packager,
            "☁️ Upload": page_upload,
            "🔄 Complete Workflow": page_workflow
        }

        selected_page = st.sidebar.radio("Navigate to", list(pages.keys()))

        # Run selected page
        pages[selected_page]()

        # Footer
        st.sidebar.markdown("---")
        st.sidebar.markdown("""
        **Skill Seekers v2.5.2**

        Convert documentation into LLM skills for:
        - Claude AI
        - Google Gemini
        - OpenAI ChatGPT
        - Generic Markdown
        """)

        st.sidebar.markdown("""
        <small>
        <a href="https://github.com/yusufkaraaslan/Skill_Seekers" target="_blank">
        GitHub Repository
        </a>
        </small>
        """, unsafe_allow_html=True)
    else:
        # Being run directly from CLI, launch streamlit
        main()
