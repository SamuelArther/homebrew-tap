class Fetchart < Formula
  desc "Download game art, achievements, posters, album covers and more from the command line"
  homepage "https://github.com/SamuelArther/fetchart"
  # Windows (brew-windows) installs the standalone build; macOS and Linux build the PyPI package below.
  url "https://github.com/SamuelArther/fetchart/releases/download/v1.6.0/fetchart-windows.exe"
  sha256 "ae5b1660ac687b5f1a78afea0d047739f03909a3ff1c34a8f580c9596f573a99"
  license "MIT"

  livecheck do
    url "https://pypi.org/pypi/fetchart/json"
    strategy :json do |json|
      json["info"]["version"]
    end
  end

  on_macos do
    url "https://files.pythonhosted.org/packages/e8/9f/aa29482a9db81a325ab9fae84feace0ba59c7199a81de5aeb461625310d0/fetchart-1.6.0.tar.gz"
    sha256 "d495ba7ebf75dc4b5136c81c66696da68ff827f78740775b77f8d1ace720efc0"

    depends_on "pillow"
    depends_on "python@3.14"
  end

  on_linux do
    url "https://files.pythonhosted.org/packages/e8/9f/aa29482a9db81a325ab9fae84feace0ba59c7199a81de5aeb461625310d0/fetchart-1.6.0.tar.gz"
    sha256 "d495ba7ebf75dc4b5136c81c66696da68ff827f78740775b77f8d1ace720efc0"

    depends_on "pillow"
    depends_on "python@3.14"
  end

  def install
    if OS.mac? || OS.linux?
      # Homebrew's Python helpers, brought in here rather than with a class-level include: older
      # brew-windows builds don't have them and would fail just loading the formula.
      extend Language::Python::Virtualenv
      virtualenv_install_with_resources
    else
      bin.install "fetchart-windows.exe" => "fetchart.exe"
    end
  end

  test do
    assert_match version.to_s, shell_output("#{bin}/fetchart --version")
  end
end
