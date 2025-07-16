generator target {
    output_type "python/pydantic"

    // Where the generated code will be saved (relative to baml_src/)
    output_dir "../"

    // What interface you prefer to use for the generated code (sync/async)
    // Both are generated regardless of the choice, just modifies what is exported
    // at the top level
    default_client_mode "sync"

    // Version of runtime to generate code for (should match installed baml-py version)
    version "0.201.0"
}
