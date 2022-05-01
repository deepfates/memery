### Core
    Need a way to reload the db and index if the root changes
        We want to allow the root to change in the same instance
            So somehow detect if root changes?
            I guess we could keep a dict that tracks multiple indexes and and databases but that could use a lot of memory. Is that bad design?

### GUI
    Should create memery object and keep it open