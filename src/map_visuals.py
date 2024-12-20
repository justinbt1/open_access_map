import click
import geopandas as gp
from matplotlib import pyplot as plt


def load_data():
    """Load polygon data from disk.
    """
    la_boundary_gdf = gp.read_file('data/local_authority_boundaries.geojson')
    crow_gdf = gp.read_file('data/defra_crow_oa.geojson')

    # Filter to only English local authority boundaries.
    la_boundary_gdf = la_boundary_gdf.loc[la_boundary_gdf['lau115cd'].str[0] == 'E']

    return la_boundary_gdf, crow_gdf


def intersect(la_boundary_gdf, crow_gdf, local_authority):
    """Find area of CROW polygons that intersect local authorities.

    Args:
        la_boundary_gdf: Geopandas local authority boundary dataframe.
        crow_gdf: Geopandas CROW open access dataframe.
        local_authority(str): Name of local authority.

    """
    la_boundary_gdf = la_boundary_gdf.loc[
        la_boundary_gdf['lau115nm'] == local_authority
    ]

    intersection_gdf = gp.overlay(
        la_boundary_gdf,
        crow_gdf,
        how="intersection"
    )

    intersection_gdf.loc[intersection_gdf['lau115nm'] == local_authority]

    return la_boundary_gdf, intersection_gdf


def plot_map(la_boundary, crow, la_name):
    """Plot local authority polgon(s) with CROW data overlayed.

    Args:
        la_boundary_gdf: Geopandas local authority boundary dataframe.
        crow_gdf: Geopandas CROW open access dataframe.
        local_authority(str): Name of local authority.

    """
    fig, ax = plt.subplots()

    la_boundary.plot(ax=ax, color='grey')
    crow.plot(ax=ax, color='green')

    fig.set_figheight(15)
    fig.set_figwidth(15)

    ax.set_axis_off()

    fig.savefig(f'outputs/map_crow_{la_name}.png', bbox_inches='tight')


@click.command()
@click.argument('local_authority', required=False)
def plot_vis(local_authority):
    """Plot local authority map.

    Args:
        local_authority(str): Name of local authority.

    """
    la_boundary, crow = load_data()

    if local_authority:
        la_boundary, crow = intersect(la_boundary, crow, local_authority)
        local_authority = '_'.join(local_authority.lower().split())
    else:
        local_authority = 'la_all'

    plot_map(la_boundary, crow, local_authority)


if __name__ == '__main__':
    plot_vis()
