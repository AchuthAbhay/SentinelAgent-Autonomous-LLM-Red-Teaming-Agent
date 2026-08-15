from security_mcp.mcp_instance import mcp

# Import tools so decorators register them
import security_mcp.tools.execute_target
import security_mcp.tools.judge_safeguard
import security_mcp.tools.judge_heuristic
import security_mcp.tools.objective_verifier


def main():
    mcp.run()


if __name__ == "__main__":
    main()