// Post Row
class PostRow extends React.Component{
  render(){
    const post = this.props.post
    // Check thumbnail
    let thumbnail;

    if (post.hero_image.thumbnail){
      thumbnail = <img src={post.hero_image.thumbnail}/>
    }
    else {
      thumbnail = "-"
    }

    return <tr>
        <td>{post.title}</td>
        <td>{thumbnail}</td>
        <td>{post.tags.join(", ")}</td>
        <td>{post.slug}</td>
        <td>{post.summary}</td>
        <td>
          <a href={`/post/${post.slug}/`}>View</a>
        </td>
    </tr>
  }
}

// Post Table
class PostTable extends React.Component{
  state = {
    dataLoaded : true,
    data : {
      results : [
        {
          id: 1,
          tags: [
            'django', 'react'
          ],
          'hero_image': {
           
          },
          title: 'Test Post',
          slug: 'test-post',
          summary: 'A test post, created for Django/React.'
        }
      ]
    }
  }

  render(){
    // Check data load
    let rows;
    if (this.state.dataLoaded){
      // Check Returned Results
      if (this.state.data.results.length){
        // Build Rows
        rows = this.state.data.results.map(post => <PostRow post={post} key={post.id}/>)
      }
      else {
        rows = <tr>
          <td colSpan="6">No Results</td>
        </tr>
      }
    }
    else {
      rows = <tr>
          <td colSpan="6">Loading Results!</td>
      </tr>
    }

    return <table
      className="table table-striped table-bordered mt-2"
    >
    <thead>
      <tr>
        <th>Title</th>
        <th>Image</th>
        <th>Tags</th>
        <th>Slug</th>
        <th>Summary</th>
        <th>Link</th>
      </tr>
      </thead>
      <tbody>
        {rows}
      </tbody>
    </table>

  }
}


const domContainer = document.getElementById("react_root")

ReactDOM.render(
  React.createElement(PostTable),
  domContainer
)