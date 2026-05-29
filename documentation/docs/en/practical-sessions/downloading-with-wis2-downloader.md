---
title: Downloading with WIS2 Downloader
---

# Downloading with WIS2 Downloader

!!! abstract "Learning outcomes!"

    By the end of this practical session, you will be able to:

    - explore and find datasets in WIS2 Downloader
    - use filtering to control the files downloaded
    - use authentication to download access-controlled datasets
    - change the default setup of WIS2 Downloader for more advanced use cases

## Introduction

In WIS2, all datasets have a metadata file that can be found in the **Global Discovery Catalogues**. As such, it is intended for users to always consult these services to find the data being shared on WIS2.

WIS2 Downloader uses this principle by finding all records available in these GDCs and combining them internally to enable the user to navigate through the data available on WIS2. As there is a large number of records to show, it is essential to provide a way for the user to filter through them and find the correct record. Even after finding and subscribing to the correct record, there may be datasets where the number of files exceeds the user's current needs. Because of this, a second level of filtering is needed — one that operates at the time of deciding whether a file should be downloaded.

## Exploring and finding in the Catalogue View

The **Catalogue View** is one of the two ways to find and subscribe to datasets in WIS2 Downloader. It aggregates records from the Global Discovery Catalogues and presents them in a searchable, filterable interface — similar to browsing a GDC portal directly.

Navigate to **Catalogue View** in the left sidebar.

![WIS2 Downloader Catalogue View](../assets/img/wis2-downloader-catalogue-view.png)

At the top of the page you will find a search bar and a set of filters. You can use these to narrow down the list of available records by keyword, centre ID, or data policy (core vs. recommended).

You can also filter spatially by defining a **bounding box** using four coordinate inputs — **North**, **West**, **South**, and **East** — expressed as decimal latitude and longitude values. When a bounding box is set, you can choose between two matching modes:

- **Intersects** — returns records whose spatial extent overlaps with the bounding box in any way.
- **Within** — returns only records whose spatial extent falls entirely inside the bounding box.

!!! note "Reloading the catalogue"

    The catalogue is loaded from the GDCs when the WIS2 Downloader starts. If you believe the list is outdated, you can force a reload from the **Settings** section in the left sidebar.

### Exercise: find and subscribe to a dataset

!!! question "Find a surface observation dataset"

    Use the filters in the Catalogue View to find a **core** surface observation dataset related to temperature and precipitation.

    1. Type `surface` in the search bar and observe how the list of records is filtered.
    2. Set the data policy filter to **core**.
    3. Set the keywords to include `temperature, precipitation` and observe how the results change.
    4. Select a record from the results to expand its details.
    5. Review the metadata shown — note the topic, the originating centre, and the data policy.
    6. Set the destination folder to `surface-obs`.
    7. Click **Subscribe** to create the subscription.

    After subscribing, navigate to **Manage Subscriptions** to confirm the new subscription appears in the list.

??? success "Click to reveal answer"

    Any record whose topic contains `surface-based-observations` and whose data policy is `core` is a valid choice. Applying the keyword filter for `temperature, precipitation` will further narrow the results to datasets relevant to those variables.

    Once subscribed, the **Manage Subscriptions** view will show the active subscription with its topic and target folder. Files will begin downloading as new notifications arrive on the broker.

!!! note "Deleting downloaded files"

    It is recommended to clean up the downloads folder after completing an exercise to free up space on the student VM:

    ```bash
    rm -fr wis2downloader/downloads/surface-obs
    ```

## Exploring and finding in the Tree View

The **Tree View** presents the WIS2 topic hierarchy as a collapsible tree, allowing you to browse available topics level by level — similar to navigating topics in MQTT Explorer. It is designed for a higher-level, top-down exploration of what data is available on WIS2, starting from the root of the hierarchy and drilling down. This contrasts with the Catalogue View, which takes you directly to individual dataset records and is better suited when you already know what you are looking for.

Navigate to **Tree View** in the left sidebar.

![WIS2 Downloader Tree View](../assets/img/wis2-downloader-tree-view.png)

The tree is organised following the WIS2 topic hierarchy. Expand each level by clicking on a node to reveal its children. At any level you can subscribe by selecting a node and clicking **Subscribe** — using a wildcard (`#`) to capture all topics below that node.

!!! note "Subscribing at different levels"

    Subscribing higher up in the tree (e.g. at the centre ID level) will capture all datasets published by that centre. Subscribing lower down gives you more granular control. Use the wildcard `#` suffix automatically appended by WIS2 Downloader when subscribing from the Tree View.

### Exercise: find and subscribe using the Tree View

!!! question "Subscribe to a dataset via the Tree View"

    Use the Tree View to find and subscribe to surface-based observation data from a specific centre.

    1. Expand the tree starting from the `cache` node, then navigate through `a` → `wis2`.
    2. Select a centre ID of your choice and continue expanding until you reach a topic related to `surface-based-observations`.
    3. Review the full topic path shown — confirm it corresponds to the dataset you want.
    4. Set the destination folder to `surface-obs-tree`.
    5. Click **Subscribe** to create the subscription.

    Navigate to **Manage Subscriptions** to confirm the subscription is active.

??? success "Click to reveal answer"

    Any topic path following the pattern `cache/a/wis2/<centre-id>/data/core/weather/surface-based-observations/#` is a valid choice. The centre ID segment will vary depending on which centre you selected in the tree.

    The **Manage Subscriptions** view will show the new subscription alongside any previously created ones.

!!! note "Deleting downloaded files"

    Clean up the downloads folder after completing the exercise:

    ```bash
    rm -fr wis2downloader/downloads/surface-obs-tree
    ```

