#!/usr/bin/env python

import argparse
import os
import sys
import subprocess
import shutil


def main():
    args = parse_args()

    rustup_bin = args.rustup_bin[0]
    rustup_home = args.rustup_home[0]
    cargo_home = args.cargo_home[0]
    manifest_path = args.manifest_path[0]
    build_path = args.build_path[0]
    platform = args.platform[0]
    is_debug = args.is_debug[0]

    build(rustup_bin, rustup_home, cargo_home, manifest_path, build_path, platform, is_debug)


def parse_args():
    parser = argparse.ArgumentParser(description='Cargo')

    parser.add_argument('--rustup_bin', nargs=1)
    parser.add_argument('--rustup_home', nargs=1)
    parser.add_argument('--cargo_home', nargs=1)
    parser.add_argument('--manifest_path', nargs=1)
    parser.add_argument('--build_path', nargs=1)
    parser.add_argument('--platform', nargs=1)
    parser.add_argument('--is_debug', nargs=1)

    args = parser.parse_args()

    # Validate rustup_bin args
    if (args.rustup_bin is None or
        len(args.rustup_bin) is not 1 or
            len(args.rustup_bin[0]) is 0):
        raise Exception("rustup_bin argument was not specified correctly")

    # Validate rustup_home args
    if (args.rustup_home is None or
        len(args.rustup_home) is not 1 or
            len(args.rustup_home[0]) is 0):
        raise Exception("rustup_home argument was not specified correctly")

    # Validate cargo_home args
    if (args.cargo_home is None or
        len(args.cargo_home) is not 1 or
            len(args.cargo_home[0]) is 0):
        raise Exception("cargo_home argument was not specified correctly")

    # Validate manifest_path args
    if (args.manifest_path is None or
        len(args.manifest_path) is not 1 or
            len(args.manifest_path[0]) is 0):
        raise Exception("manifest_path argument was not specified correctly")

    # Validate build_path args
    if (args.build_path is None or
        len(args.build_path) is not 1 or
            len(args.build_path[0]) is 0):
        raise Exception("build_path argument was not specified correctly")

    if "out" not in args.build_path[0]:
        raise Exception("build_path did not contain 'out'")

    # Validate platform args
    if (args.platform is None or
        len(args.platform) is not 1 or
            len(args.platform[0]) is 0):
        raise Exception("platform argument was not specified correctly")

    # Validate is_debug args
    if (args.is_debug is None or
        len(args.is_debug) is not 1 or
            len(args.is_debug[0]) is 0):
        raise Exception("is_debug argument was not specified correctly")

    if (args.is_debug[0] != "false" and args.is_debug[0] != "true"):
        raise Exception("is_debug argument was not specified correctly")

    # args are valid
    return args


def build(rustup_bin, rustup_home, cargo_home, manifest_path, build_path, platform, is_debug):
    targets = []

    if platform == "Windows x86":
        targets = ["i686-pc-windows-msvc"]
    elif platform == "Windows x64":
        targets = ["x86_64-pc-windows-msvc"]
    elif platform == "macOS x64":
        targets = ["x86_64-apple-darwin"]
    elif platform == "Linux x64":
        targets = ["x86_64-unknown-linux-gnu"]
    elif platform == "Android arm":
        targets = ["arm-linux-androideabi"]
    elif platform == "Android arm64":
        targets = ["aarch64-linux-android"]
    elif platform == "Android x86":
        targets = ["i686-linux-android"]
    elif platform == "Android x64":
        targets = ["x86_64-linux-android"]
    elif platform == "iOS":
        targets = ["aarch64-apple-ios", "x86_64-apple-ios"]
    else:
        raise ValueError('Cannot build due to unknown platform')

    # Set environment variables for rustup
    env = os.environ.copy()
    env['PATH'] = rustup_bin + os.pathsep + env['PATH']
    env['RUSTUP_HOME'] = rustup_home
    env['CARGO_HOME'] = cargo_home

    # Set environment variables for Challenge Bypass Ristretto FFI
    env['NO_CXXEXCEPTIONS'] = "1"
    if is_debug == "false":
        env['NDEBUG'] = "1"

    # Build targets
    for target in targets:
        args = []
        args.append("cargo")
        args.append("build")
        if is_debug == "false":
            args.append("--release")
        args.append("--manifest-path=" + manifest_path)
        args.append("--target-dir=" + build_path)
        args.append("--target=" + target)

        try:
          subprocess.check_call(args, env=env)
        except subprocess.CalledProcessError as e:
          print e.output
          raise e


if __name__ == '__main__':
    sys.exit(main())